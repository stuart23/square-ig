from datetime import UTC, datetime
from decimal import Decimal

from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from utils import getenv_or_raise
from auth.token_queue import publish


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

        This is a full table scan, which sucks, but I need a better index
        to search.

        Return looks like:
        ```
        {
            'Items': [],
            'Count': 0,
            'ScannedCount': 0,
            'ResponseMetadata': {}
        }
        ```
        """
        now_timestamp = Decimal(datetime.now(UTC).timestamp())
        response = self._table.scan(
            FilterExpression=Attr('refresh_after_stamp').lt(now_timestamp),
            )
        return response
