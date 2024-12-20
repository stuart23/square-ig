from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient

from json import dumps
from hashlib import sha256
from time import sleep, time
from uuid import uuid4

from catalog import Item
from utils import batch, get_secret


SQUARE_TOKEN_ARN_ENV = "square_token_arn"


def get_square_client():
    '''
    Gets the the square API key from AWS secrets manager and return a client with that.
    '''
    square_token = get_secret(SQUARE_TOKEN_ARN_ENV)
    return SquareClient(
        bearer_auth_credentials=BearerAuthCredentials(
            access_token=square_token
        ),
        environment='production'
    )


def get_catalog_items():
    '''
    Returns a generator of all the catalog items.
    '''
    items = _get_all_catalog_items()

    for item in items:
        item_data = item['item_data']
        item_str = item_data['name']
        for variation in item_data['variations']:
            # Try and get the pet_safe status from the variation
            item_details = {'item_str': item_str, 'pet_safe': False}
            for custom_attribute in variation.get('custom_attribute_values', {}).values():
                if custom_attribute.get('name', '') == 'Pet Safe':
                    item_details['pet_safe'] = custom_attribute['boolean_value']
                    break
            item_variation_data = variation['item_variation_data']
            item_details['sku'] = item_variation_data.get('sku')
            item_details['variation_str'] = item_variation_data['name']
            item_details['item_id'] = item_variation_data["item_id"]
            item_details['variation_id'] = variation['id']
            try:
                item_details['price'] = item_variation_data['price_money']['amount']
            except KeyError:
                item_details['price'] = 0
            yield Item(**item_details)


def _get_all_catalog_items():
    """
    Retrieves all catalog items as a generator.
    """

    cursor = None
    catalog = get_square_client().catalog

    while True:
        response = catalog.list_catalog(
            cursor=cursor,
            types="ITEM"
        )

        if response.is_success():
            objects = response.body["objects"]
            for object in objects:
                yield object
            cursor = response.body.get("cursor")

            if cursor is None:
                break  # No more pages
        else:
            raise Exception(f"Could not retrieve objects due to: {response.errors}")
            break  # Stop on error

    return objects


@batch(batch_size=500)
def patch_objects_sku(items):
    '''
    Updates multiple objects sku.
    '''
    print('Patching {0} records in Square'.format(len(items)))
    catalog = get_square_client().catalog
    item_map = {item.variation_id: item.sku for item in items}
    response = catalog.batch_retrieve_catalog_objects(
        body={
            "object_ids":list(item_map.keys()),
            "include_related_objects":False,
            "catalog_version":None,
            "include_category_path_to_root":False
        }
    )
    square_items = response.body['objects']
    objects = []
    for item in square_items:
        item_variation_data = item['item_variation_data']
        item_variation_data['sku'] = item_map[item['id']]
        objects.append(
            {
                'type': 'ITEM_VARIATION',
                'id': item['id'],
                'version': item['version'],
                'item_variation_data': item_variation_data
            }
        )
    upsert_response = catalog.batch_upsert_catalog_objects({
        "idempotency_key": str(uuid4()),
        "batches": [
            {"objects": objects}
        ]
    })
    if upsert_response.is_success():
        return
    else:
        raise Exception(f'Could not upsert item {item} due to: {upsert_response.errors}')


def create_catalog_image(item, image):
    pass
    # catalog = get_square_client().catalog
    # item_name = "{0} - {1}".format(item.item_str, item.variation_str)
    # print(f'Saving image to item: {item}')
    # for try_number in range(5):
    #     response = catalog.create_catalog_image(
    #         request={
    #             "idempotency_key": generate_idempotency_key(item),
    #             "object_id": item.item_id,
    #             "image": {
    #                 "type": "ITEM",
    #                 "id": "#TEMP_ID",
    #                 "image_data": {
    #                     "name": item_name,
    #                     "sku": item.sku,
    #                     "caption": "QR Code"
    #                 },
    #                 "type": "IMAGE",
    #                 "is_deleted": False,
    #             }
    #         },
    #         image_file=image
    #     )
    #     if response.is_success():
    #         return response
    #     elif any([x['category'] == 'RATE_LIMIT_ERROR' for x in response.errors]):
    #         sleep_time = 10 * try_number
    #         print(f'Upload failed due to rate limit. Waiting {sleep_time} seconds to retry')
    #         sleep(sleep_time)
    # else:
    #     raise Exception(f'Could not add image to item {item} due to: {response.errors}')


def generate_idempotency_key(item):
    """
    Creates an idempotency key by hashing the dict.
    """
    return sha256(dumps({"item": item.__dict__, "timestamp": time()}, sort_keys=True).encode('utf-8')).hexdigest()


def getInstagramHandle(customer_id):
    '''
    Takes the Square customer ID and returns the instagram handle if it is recorded, otherwise 
    it raises a ValueError.
    '''
    customer_custom_attributes = get_square_client().customer_custom_attributes
    response = customer_custom_attributes.list_customer_custom_attribute_definitions()
    if response.errors:
        raise ValueError(f'Could not find Instagram Handle Attribute due to: {response.errors}')
    custom_attribute_definitions = response.body['custom_attribute_definitions']

    instagram_handle_attributes = [attribute for attribute in custom_attribute_definitions if attribute['name'] == 'Instagram Handle']
    if len(instagram_handle_attributes) != 1:
        raise ValueError(f'Could not find Instagram Handle in the Customer Custom Attributes list: {custom_attribute_definitions}')
    instagram_handle_key = instagram_handle_attributes[0]['key']

    response = customer_custom_attributes.retrieve_customer_custom_attribute(
        customer_id=customer_id,
        key=instagram_handle_key
    )
    if response.errors:
        raise ValueError(f'Could not find Instagram Handle for Customer {customer_id}. Error is {response.errors}')
    
    return response.body['custom_attribute']['value']