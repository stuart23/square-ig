from boto3 import resource
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table = resource("dynamodb").Table("catalog")

def upsert_by_sku(sku, price, item_str, variation_str, item_id):
    """
    If an object does not exist in the database, it will be added.

    Right now this loops over all the items, but we should be able to do a query
    to find out all the items that don't exist in dynamo.

    We should also check that all the fields for each object are the same.

    Returns True if the item was updated, otherwise False
    """
    response = table.query(
        KeyConditionExpression=(
            Key("SKU").eq(sku)
        ),
    )
    if response['Count'] == 0:
        # No item with this sku exists.
        print(f'Adding item to DynamoDB: {item_str} - {variation_str}')
        table.put_item(
                Item={
                    "SKU": sku,
                    "price": Decimal(str(price)),
                    "item_str": item_str,
                    "variation_str": variation_str,
                    "item_id": item_id
                }
            )
        return True
    elif response['Count'] > 1:
        raise Exception(f'There are multiple entries in Dynamo with the same SKU: {sku}')
    else:
        return False