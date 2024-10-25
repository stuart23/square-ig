from boto3 import client as Boto3Client
from json import loads
from square_client import get_all_catalog_items, upsert_catalog_object
from catalog_dynamodb import upsert_by_sku
from catalog_queue import publish

URL_PREFIX = "plantsoc.io"


def handler(event, context):
    items = get_all_catalog_items()

    for item in items:
        if any([upsert_sku(variation) for variation in item['item_data']['variations']]):
            print("One or more variation SKUs were updated. Upserting item to square.")
            upsert_catalog_object(item)
        item_str = item['item_data']['name']
        for variation in item['item_data']['variations']:
            # Try and get the pet_safe status from the variation
            pet_safe = False
            for custom_attribute in variation.get('custom_attribute_values', {}).values():
                if custom_attribute.get('name', '') == 'Pet Safe':
                    pet_safe = custom_attribute['boolean_value']
                    break
            item_variation_data = variation['item_variation_data']
            sku = item_variation_data['sku']
            variation_str = item_variation_data['name']
            item_id = item_variation_data["item_id"]
            try:
                price = item_variation_data['price_money']['amount']/100
            except:
                price = 0
            details = {
                "sku": sku,
                "price": price,
                "item_str": item_str,
                "variation_str": variation_str,
                "item_id": item_id,
                "pet_safe": pet_safe
            }
            if upsert_by_sku(**details):
                publish(details)

def upsert_sku(variation):
    """
    Rewrites the sku with the format URL_PREFIX/old_sku
    """
    item_variation_data = variation['item_variation_data']
    sku = item_variation_data['sku']
    if sku.startswith(URL_PREFIX):
        return False
    elif item_variation_data['name'].startswith('no_sku'):
        return False
    else:
        new_sku = '/'.join([URL_PREFIX, sku])
        print(f"SKU {sku} does not start with {URL_PREFIX}. Updating to {new_sku}")
        variation['item_variation_data']['sku'] = new_sku
        return True


if __name__ == "__main__":
    handler(None, None)