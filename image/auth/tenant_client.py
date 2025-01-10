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
        response = self.get_merchant(merchant_id)
        if response["Count"] == 0:
            # No item with this sku exists.
            print(f"Adding item to DynamoDB: {merchant_id}")
            self._table.put_item(Item={"merchant_id": merchant_id, **args})
            return True
        if response["Count"] > 1:
            raise Exception(
                "There are multiple entries in Dynamo with the same "
                f"merchant_id: {merchant_id}"
            )
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

    def get_merchant(self, merchant_id, check_single=False):
        '''
        Returns details on a merchant.

        If check_single is true, will test to make sure that there is
        exactly one record and will raise an exception if that is not true.
        '''
        response = self._table.query(
            KeyConditionExpression=(Key("merchant_id").eq(merchant_id)),
        )
        if not check_single:
            return response
        if response["Count"] == 0:
            raise ValueError(f'No merchant found for {merchant_id}')
        elif response["Count"] > 1:
            raise ValueError(f'More than one merchant found for {merchant_id}')
        return response