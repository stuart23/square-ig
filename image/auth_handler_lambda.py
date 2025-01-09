from datetime import datetime, UTC
from decimal import Decimal

from auth import TenantClient, TokenServices
from utils import SQSDeserialize


def handler(event, context):
    '''
    All messages on the auth SQS topic will trigger this lambda. Depending
    on what is in the message, a different function will be launched.
    Current actions are:
    - new_connection: Triggered when a new oauth connection is made.
    - find_tokens_to_refresh: Triggered on the aws eventbridge scheduler to
        periodically check what tokens need to be refreshed.
    '''
    for body in SQSDeserialize(event):
        action = body["action"]
        if action == "new_connection":
            new_connection(**body["data"])
        elif action == "find_tokens_to_refresh":
            find_tokens_to_refresh()
        else:
            raise ValueError(f"No function for action {action}")


def new_connection(**args):
    token_services = TokenServices()
    try:
        token_details = token_services.get_token(args["code"])
    except token_services.ExpiredAuthCode:
        print("Token auth code has expired. Skipping this exchange.")
        return
    print(
        "Token successfully retrieved for merchant {merchant_id}".format(
            **token_details
        )
    )
    # Not going to catch the exception on this because IDK what to do if it is
    # not an iso date
    expires_at = datetime.fromisoformat(token_details["expires_at"])
    refresh_after = token_services.get_refresh_after(expires_at)
    tenant_client = TenantClient()
    now = datetime.now(UTC)
    tenant_client.upsert_tenant(
        access_token=token_details["access_token"],
        token_type=token_details["token_type"],
        issued_at=str(now),
        issued_at_stamp=Decimal(now.timestamp()),
        expires_at=str(expires_at),
        expires_at_stamp=Decimal(expires_at.timestamp()),
        refresh_after=str(refresh_after),
        refresh_after_stamp=Decimal(refresh_after.timestamp()),
        merchant_id=token_details["merchant_id"],
        refresh_token=token_details["refresh_token"],
    )


def find_tokens_to_refresh():
    '''
    Reads the database to see if there are any tokens that need to be
    refreshed.
    '''
    print('Finding tokens to refresh')
