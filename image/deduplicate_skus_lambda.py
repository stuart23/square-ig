from square_client import get_catalog_items, patch_objects_sku
from catalog.catalog_dynamodb import get_needs_label_items, get_website_needs_update_items, set_website_true, upsert_by_id
from catalog.catalog_queue import publish
from descriptions import DescriptionsGit


def handler(event, context):
    items = get_catalog_items()
    update_items = []
    for item in items:
        # Check to see that the sku is not already in use. Will add it to the list if it is duplicated.
        old_sku = item.sku
        if not item.validate_sku():
            update_items.append(item)
            upsert_by_id(item)
    if update_items:
        print(f'Updating {len(update_items)} items.')
        patch_objects_sku(update_items)
    else:
        print('No duplicate skus found.')


if __name__ == "__main__":
    handler(None, None)