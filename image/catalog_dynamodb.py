from boto3 import resource
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table = resource("dynamodb").Table("catalog")

def upsert_by_sku(sku, price, item_str, variation_str):
    """
    If an object does not exist in the database, it will be added.

    Right now this loops over all the items, but we should be able to do a query
    to find out all the items that don't exist in dynamo.
    """
    response = table.query(
        KeyConditionExpression=(
            Key("SKU").eq(sku)
        ),
    )
    if response['Count'] == 0:
        # No item with this sku exists.
        try:
            price = variation['item_variation_data']['price_money']['amount'] / 100
        except KeyError:
            price = 0
        print(f'Adding item to DynamoDB: {variation}')
        table.put_item(
                Item={
                    "SKU": sku,
                    "price": Decimal(str(price)),
                    "item_str": item_str,
                    "variation_str": variation_str
                }
            )
    elif response['Count'] > 1:
        raise Exception(f'There are multiple entries in Dynamo with the same SKU: {sku}')