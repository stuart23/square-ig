from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient
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
    catalog.upsert_catalog_object(item)
    if response.is_success():
        return
    else:
        raise Exception(f'Could not upsert item {item}')