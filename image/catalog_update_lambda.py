from square_client import get_catalog_items, patch_objects_sku
from catalog.catalog_dynamodb import get_needs_label_items, get_website_needs_update_items, set_website_true, upsert_by_id
from catalog.catalog_queue import publish
from descriptions import DescriptionsGit


def handler(event, context):
    items = get_catalog_items()
    for item in items:
        # update the sku with the url format or generate one if it doesn't exist.
        # If the sku is modified, that sku is then upserted into square.
        if item.update_sku():
            validate_sku(item)
            patch_objects_id(item)
        upsert_by_id(item)

    needs_label_items = get_needs_label_items()
    for item in needs_label_items:
        publish(item.__dict__)

    # Generate website descriptions for new items
    website_needs_update_items = get_website_needs_update_items()
    descriptions = DescriptionsGit()
    for item in website_needs_update_items:
        descriptions.add_item(item)
        set_website_true(item)
    descriptions.commit()

if __name__ == "__main__":
    handler(None, None)