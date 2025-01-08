from auth import TenantClient
from utils import SQSDeserialize

def handler(event, context):
    for body in SQSDeserialize(event):
        action = body['action']
        if action == 'new_connection':
            new_connection(**body['data'])
        else:
            raise ValueError(f'No function for action {action}')


def new_connection(**args):
    tenant_client = TenantClient()
    tenant_client.upsert_tenant(args)