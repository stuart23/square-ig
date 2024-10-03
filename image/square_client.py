from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient
from json import dumps
from hashlib import sha256
from boto3 import client as Boto3Client

SECRET_NAME = "square_token"

boto3_client = Boto3Client('secretsmanager')
response = boto3_client.get_secret_value(SecretId=SECRET_NAME)
square_token = response['SecretString']

client = SquareClient(
    bearer_auth_credentials=BearerAuthCredentials(
        access_token=square_token
    ),
    environment='production'
)
catalog = client.catalog
customer_custom_attributes = client.customer_custom_attributes

def get_all_catalog_items():
    """Retrieves all catalog items using pagination."""

    cursor = None
    objects = []

    while True:
        response = catalog.list_catalog(
            cursor=cursor,
            types="ITEM"
        )

        if response.is_success():
            objects.extend(response.body["objects"])
            cursor = response.body.get("cursor")

            if cursor is None:
                break  # No more pages
        else:
            print(f"Error: {response.errors}")
            break  # Stop on error

    return objects


def upsert_catalog_object(item):

    response = catalog.upsert_catalog_object({
        "idempotency_key": generate_idempotency_key(item),
        "object": item
    })
    if response.is_success():
        return
    else:
        raise Exception(f'Could not upsert item {item}')


def create_catalog_image(item, image):
    return catalog.create_catalog_image(
        request={
            "idempotency_key": generate_idempotency_key(item),
            "object_id": item['item_id'],
            "image": {
                "type": "ITEM",
                "id": "#TEMP_ID",
                "image_data": {
                    "caption": "QR Code"
                },
                "type": "IMAGE",
                "is_deleted": False,
            }
        },
        image_file=image
    )


def generate_idempotency_key(item):
    """
    Creates an idempotency key by hashing the dict.
    """
    return sha256(dumps(item, sort_keys=True).encode('utf-8')).hexdigest()


def getInstagramHandle(customer_id):
    '''
    Takes the Square customer ID and returns the instagram handle if it is recorded, otherwise 
    it raises a ValueError.
    '''
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