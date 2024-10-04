from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient
from os import getenv

from json import dumps
from hashlib import sha256
from boto3 import client as Boto3Client
from time import time


SQUARE_TOKEN_ARN_ENV = "square_token_arn"


def get_square_client():
    '''
    Gets the the square API key from AWS secrets manager and return a client with that.
    '''
    credentials_arn = getenv(SQUARE_TOKEN_ARN_ENV)
    secretsmanager_client = Boto3Client('secretsmanager')
    square_token = secretsmanager_client.get_secret_value(SecretId=credentials_arn)['SecretString']
    return SquareClient(
        bearer_auth_credentials=BearerAuthCredentials(
            access_token=square_token
        ),
        environment='production'
    )


def get_all_catalog_items():
    """Retrieves all catalog items using pagination."""

    cursor = None
    objects = []
    catalog = get_square_client().catalog

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
    catalog = get_square_client().catalog

    response = catalog.upsert_catalog_object({
        "idempotency_key": generate_idempotency_key(item),
        "object": item
    })
    if response.is_success():
        return
    else:
        raise Exception(f'Could not upsert item {item} due to: {response.errors}')


def create_catalog_image(item, image):
    catalog = get_square_client().catalog
    item_name = "{0} - {1}".format(item['item_str'], item['variation_str'])
    item_id = item['item_id']
    print(f'Saving image to item: {item_id}: {item_name}')
    response = catalog.create_catalog_image(
        request={
            "idempotency_key": generate_idempotency_key(item),
            "object_id": item['item_id'],
            "image": {
                "type": "ITEM",
                "id": "#TEMP_ID",
                "image_data": {
                    "name": item_name,
                    "caption": "QR Code"
                },
                "type": "IMAGE",
                "is_deleted": False,
            }
        },
        image_file=image
    )
    if response.is_success():
        return response
    else:
        raise Exception(f'Could not add image to item {item_id} due to: {response.errors}')


def generate_idempotency_key(item):
    """
    Creates an idempotency key by hashing the dict.
    """
    return sha256(dumps({"item": item, "timestamp": time()}, sort_keys=True).encode('utf-8')).hexdigest()


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