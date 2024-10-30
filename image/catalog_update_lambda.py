from boto3 import client as Boto3Client
from json import loads
from square_client import get_all_catalog_items, upsert_catalog_object
from catalog.catalog_dynamodb import upsert_by_sku
from catalog.catalog_queue import publish
from descriptions.create_description import InstructionsGit


def handler(event, context):
    items = get_catalog_items()
    for item in items:
        print(item)
        # update the sku with the url format or generate one if it doesn't exist.
        # If the sku is modified, that sku is then upserted into square.
        if item.update_sku():
            upsert_catalog_object(item)
        upsert_by_sku(item)


if __name__ == "__main__":
    handler(None, None)