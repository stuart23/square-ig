from boto3 import resource
from boto3.dynamodb.conditions import Key


class TenantClient(object):
    def __init__(self):
        self._table = resource("dynamodb").Table("tenants")


    def upsert_tenant(sku, oauth_code):
        """
        If an object does not exist in the database, it will be added.
        """
        response = table.query(
            KeyConditionExpression=(
                Key("oauth_code").eq(oauth_code)
            ),
        )
        if response['Count'] == 0:
            # No item with this sku exists.
            print(f'Adding item to DynamoDB: {oauth_code}')
            table.put_item(
                    Item={
                        "oauth_code": oauth_code,
                    }
                )
            return True
        elif response['Count'] > 1:
            raise Exception(f'There are multiple entries in Dynamo with the same oauth_code: {oauth_code}')
        else:
            return False