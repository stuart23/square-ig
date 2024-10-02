from boto3 import resource
from boto3.dynamodb.conditions import Key

table = resource("dynamodb").Table("catalog")

def get_by_sku(sku):
    response = table.query(
        ProjectionExpression="#yr, title, info.genres, info.actors[0]",
        ExpressionAttributeNames={"#yr": "year"},
        KeyConditionExpression=(
            Key("sku").eq(sku)
        ),
    )
    return response