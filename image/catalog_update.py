from boto3 import client as Boto3Client
from json import loads
from square_client import get_all_catalog_items, upsert_catalog_object
from catalog_dynamodb import get_by_sku

URL_PREFIX = "plantsoc.io"

def handler(event, context):
    items = get_all_catalog_items()

    for item in items:
        if any([upsert_sku(variation) for variation in item['item_data']['variations']]):
            print("One or more variation SKUs were updated. Upserting item to square.")
            upsert_catalog_object(item)
        for variation in item['item_data']['variations']:
            response = get_by_sku(variation['sku'])
            print('sku')
            print('response')


def upsert_sku(variation):
    """
    Rewrites the sku with the format URL_PREFIX/old_sku
    """
    sku = variation['item_variation_data']['sku']
    if sku.startswith(URL_PREFIX):
        return False
    else:
        new_sku = '/'.join([URL_PREFIX, sku])
        print(f"SKU {sku} does not start with {URL_PREFIX}. Updating to {new_sku}")
        variation['item_variation_data']['sku'] = new_sku
        return True