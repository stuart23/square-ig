from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient
from boto3 import client as Boto3Client

SECRET_NAME = "square_token"

boto3_client = Boto3Client('secretsmanager')
square_token = boto3_client.get_secret_value(SecretId=SECRET_NAME)

client = SquareClient(
    bearer_auth_credentials=BearerAuthCredentials(
        access_token=square_token
    ),
    environment='Production'
)


def get_all_catalog_objects():
    """Retrieves all catalog objects using pagination."""

    catalog_api = client.catalog_api
    cursor = None
    objects = []

    while True:
        response = catalog_api.search_catalog_objects(
            body={
                "cursor": cursor,
                "limit": 100  # Adjust limit as needed
            }
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