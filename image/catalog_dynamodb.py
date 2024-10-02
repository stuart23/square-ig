from boto3 import resource
from boto3.dynamodb.conditions import Key
from decimal import Decimal

table = resource("dynamodb").Table("catalog")

def upsert_by_sku(variation):
    sku = variation['item_variation_data']['sku']
    response = table.query(
        # ProjectionExpression="#yr, title, info.genres, info.actors[0]",
        # ExpressionAttributeNames={"#yr": "year"},
        KeyConditionExpression=(
            Key("SKU").eq(sku)
        ),
    )
    if response['Count'] == 0:
        try:
            price = variation['item_variation_data']['price_money']['amount'] / 100
        except KeyError:
            price = 0
        import pdb; pdb.set_trace()
        table.put_item(
                Item={
                    "SKU": sku,
                    "price": Decimal(str(price)),
                }
            )
    elif response['Count'] > 1:
        raise Exception(f'There are multiple entries in Dynamo with the same SKU: {sku}')