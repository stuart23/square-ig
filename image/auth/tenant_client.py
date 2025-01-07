from boto3 import resource
from boto3.dynamodb.conditions import Key
from utils import getenv_or_raise


class TenantClient(object):
    def __init__(self):
        TABLE = getenv_or_raise('TENANTS_TABLE')
        self._table = resource("dynamodb").Table(TABLE)


    def upsert_tenant(self, oauth_code):
        """
        If an object does not exist in the database, it will be added.
        """
        response = self._table.query(
            KeyConditionExpression=(
                Key("oauth_code").eq(oauth_code)
            ),
        )
        if response['Count'] == 0:
            # No item with this sku exists.
            print(f'Adding item to DynamoDB: {oauth_code}')
            self._table.put_item(
                    Item={
                        "oauth_code": oauth_code,
                    }
                )
            return True
        elif response['Count'] > 1:
            raise Exception(f'There are multiple entries in Dynamo with the same oauth_code: {oauth_code}')
        else:
            return False