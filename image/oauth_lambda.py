from tenant_client import TenantClient

def handler(event, context):
    '''
    Adds the tenant to the dynamo table.
    '''
    if code := event['queryStringParameters'].get('code'):
        TenantClient().upsert_tenant(oauth_code=code)