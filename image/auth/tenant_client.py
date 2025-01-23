from datetime import UTC, datetime
from decimal import Decimal

from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from utils import getenv_or_raise
from auth.token_queue import publish
from auth.token_services import TokenServices


class TenantClient(object):
    def __init__(self):
        table_name = getenv_or_raise("tenants_table_name")
        self._table = resource("dynamodb").Table(table_name)

    def upsert_token(self, token_details):
        """
        Input is what is returned from a square API call to the token
        endpoint. The results plus some extra details are then written
        to dynamo.

        If there is already an entry for that merchant, it is updated,
        otherwise a new merchant is added.
        """
        # Not going to catch the exception on this because IDK what to do if
        # it is not an iso date.
        expires_at = datetime.fromisoformat(token_details["expires_at"])
        refresh_after = TokenServices.get_refresh_after(expires_at)
        now = datetime.now(UTC)

        merchant_id = token_details["merchant_id"]

        args = {
            'access_token': token_details["access_token"],
            'token_type': token_details["token_type"],
            'issued_at': str(now),
            'issued_at_stamp': Decimal(now.timestamp()),
            'expires_at': str(expires_at),
            'expires_at_stamp': Decimal(expires_at.timestamp()),
            'refresh_after': str(refresh_after),
            'refresh_after_stamp': Decimal(refresh_after.timestamp()),
            'refresh_token': token_details["refresh_token"],
        }
        merchants = self.get_merchant(merchant_id)
        if len(merchants) == 0:
            # No item with this sku exists.
            print(f"Adding item to DynamoDB: {merchant_id}")
            self._table.put_item(Item={"merchant_id": merchant_id, **args})
            return True
        if len(merchants) == 1:
            # Merchant already exists in db. Patching.
            print(f"Patching item to DynamoDB: {merchant_id}")
            inputs = self._generate_dynamo_update_props(args)
            self._table.update_item(
                Key={"merchant_id": merchant_id},
                UpdateExpression=inputs['UpdateExpression'],
                ExpressionAttributeValues=inputs['ExpressionAttributeValues'],
            )
            return True
        if len(merchants) > 1:
            raise Exception(
                "There are multiple entries in Dynamo with the same "
                f"merchant_id: {merchant_id}"
            )

        return False

    @staticmethod
    def _generate_dynamo_update_props(attrs):
        '''
        The dynamo update requires a crazy string and dict, so we create it
        not inline so it can be tested.
        '''
        UpdateExpression = 'set ' + ', '.join(
            [f'{key}=:{key}' for key in attrs.keys()]
        )
        ExpressionAttributeValues = {
            f':{key}': value for key, value in attrs.items()
        }
        return {
            'UpdateExpression': UpdateExpression,
            'ExpressionAttributeValues': ExpressionAttributeValues
        }

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

    def get_merchant(self, merchant_id, single_record=False):
        '''
        Returns details on a merchant.

        If single_record is true, will test to make sure that there is
        exactly one record and will raise an exception if that is not true.
        '''
        response = self._table.query(
            KeyConditionExpression=(Key("merchant_id").eq(merchant_id)),
        )
        if not single_record:
            return response['Items']
        if response["Count"] == 0:
            raise ValueError(f'No merchant found for {merchant_id}')
        elif response["Count"] > 1:
            raise ValueError(f'More than one merchant found for {merchant_id}')
        return response['Items'][0]
