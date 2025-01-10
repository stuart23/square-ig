from boto3 import resource
from boto3.dynamodb.conditions import Key
from utils import getenv_or_raise
from datetime import datetime, UTC
from decimal import Decimal


class TenantClient(object):
    def __init__(self):
        table_name = getenv_or_raise("tenants_table_name")
        self._table = resource("dynamodb").Table(table_name)

    def upsert_tenant(self, merchant_id, **args):
        """
        If an object does not exist in the database, it will be added.
        """
        response = self._table.query(
            KeyConditionExpression=(Key("merchant_id").eq(merchant_id)),
        )
        if response["Count"] == 0:
            # No item with this sku exists.
            print(f"Adding item to DynamoDB: {merchant_id}")
            self._table.put_item(Item={"merchant_id": merchant_id, **args})
            return True
        elif response["Count"] > 1:
            raise Exception(
                "There are multiple entries in Dynamo with the same "
                f"merchant_id: {merchant_id}"
            )
        else:
            return False

    def find_tokens_to_refresh(self):
        """
        Gets all the tenants with tokens that have refresh_after dates in
        the past.
        """
        now_timestamp = Decimal(datetime.now(UTC).timestamp())
        response = self._table.query(
                ProjectionExpression="#refresh_after_stamp, merchant_id",
                ExpressionAttributeNames={
                    "#refresh_after_stamp": "refresh_after_stamp"
                },
                KeyConditionExpression=(
                    Key("refresh_after_stamp").lt(now_timestamp)
                ),
            )
        return response