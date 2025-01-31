from square_client import SquareClient
from catalog.catalog_dynamodb import (
    get_needs_label_items,
    get_website_needs_update_items,
    set_website_true,
    upsert_by_id,
)
from catalog.catalog_queue import publish
from descriptions import DescriptionsGit
from auth import TenantClient
from utils import should_mutate_sku

from json import loads


def handler(event, context):
    '''
    If the merchant record has update_skus set to true for the env
    (e.g. dev_update_skus), then skus will be mutated.
    '''
    records = event['Records']
    tenant_client = TenantClient()

    for record in records:
        body = loads(record['body'])
        merchant_id = body['merchant_id']
        print(f'Updating catalog for Merchant ID: {merchant_id}')
        merchant_details = tenant_client.get_merchant(
            merchant_id, single_record=True
        )
        access_token = merchant_details['access_token']
        square_client = SquareClient(access_token)
        items = square_client.get_catalog_items()

        update_skus = should_mutate_sku(merchant_details)
        update_items = []
        for item in items:
            # update the sku with the url format or generate one if it doesn't
            # exist. If the sku is modified, that sku is then upserted into
            # square.
            if update_skus and item.update_sku():
                print("Updating SKU for item {item}")
                item.validate_sku()
                update_items.append(item)
            else:
                # Dirty patch so we can create skus for items even if they're
                # not mutated in square
                item.validate_sku()
            upsert_by_id(item)
        if update_items:
            square_client.patch_objects_sku(items=update_items)
    return
    needs_label_items = get_needs_label_items()
    for item in needs_label_items:
        publish(item.__dict__)

    # Generate website descriptions for new items - this should probably be another function triggered by an sns
    website_needs_update_items = get_website_needs_update_items()
    descriptions = DescriptionsGit()
    new_items = False
    for item in website_needs_update_items:
        descriptions.add_item(item)
        set_website_true(item)
        new_items = True
    if new_items:
        print(
            "Items needed their description updated - Adding the directory and committing."
        )
        descriptions.update_directory(square_client.get_catalog_items())
        descriptions.commit()


if __name__ == "__main__":
    handler(None, None)
