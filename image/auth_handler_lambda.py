
from auth import TenantClient, TokenServices
from utils import SQSDeserialize


def handler(event, context):
    for body in SQSDeserialize(event):
        action = body['action']
        if action == 'new_connection':
            new_connection(**body['data'])
        else:
            raise ValueError(f'No function for action {action}')


def new_connection(**args):
    token_services = TokenServices()
    try:
        token_details = token_services.get_token(args['code'])
    except token_services.ExpiredAuthCode
        print('Token auth code has expired. Skipping this exchange.')
        return
    print('Token successfully retrieved for merchant {merchant_id}'.format(**token_details))
    # Not going to catch the exception on this because IDK what to do if it is not an iso date
    expires_at = datetime.fromisoformat(token_details['expires_at'])
    refresh_after = token_services.get_refresh_after(expires_at)
    tenant_client = TenantClient()
    tenant_client.upsert_tenant(
        access_token=token_details['access_token'],
        token_type=token_details['token_type'],
        expires_at=expires_at,
        expires_at_stamp=expires_at.timestamp(),
        refresh_after=refresh_after,
        refresh_after_stamp=refresh_after.timestamp(),
        merchant_id=token_details['merchant_id'],
        refresh_token=token_details['refresh_token']
    )