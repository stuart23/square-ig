from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client as SquareClient
from boto3 import client as Boto3Client


def get_square_client():
    '''
    Gets the the square API key from AWS secrets manager and return a client with that.
    '''
    credentials_arn = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
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


if __name__ == '__main__':
    items = get_all_catalog_items()
    catalog = get_square_client().catalog

    for item in items:
        images = item['item_data']['image_ids']
        for image_id in images:
            image = catalog.retrieve_catalog_object(
                object_id=image_id,
                include_related_objects=False,
                catalog_version=None,
                include_category_path_to_root=False
            )
            try:
                caption = image.body['object']['image_data']['caption']
            except KeyError:
                continue
            if caption == 'QR Code':
                catalog.delete_catalog_object(object_id=image_id)