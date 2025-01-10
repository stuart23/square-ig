from datetime import datetime, timedelta, UTC
from json import loads

from square.client import Client
from utils import get_secret
from utils import MetricsHandler

SQUARE_QR_CODES_CREDENTIALS_ARN = "square_qr_codes_credentials_arn"


class TokenServices:
    class ExpiredAuthCode(Exception):
        """
        Exception raised if Square rejects the request because the Auth Code
        has expired.
        """

        def __str__(self):
            return "Authorization Code has expired"

    class UnknownAPIError(Exception):
        """
        Exception raised if Square rejects the request for an unknown reason.
        """

        def __str__(self):
            return "Unknown API Error"

    def __init__(self, client_id=None, client_secret=None):
        """
        Pass in BOTH square application credentials otherwise they will be
        retrieved from the secret referenced in the envvar set above in
        SQUARE_QR_CODES_CREDENTIALS_ARN.
        """
        if not client_id and not client_secret:
            credentials = loads(get_secret(SQUARE_QR_CODES_CREDENTIALS_ARN))
            self.client_id = credentials["client_id"]
            self.client_secret = credentials["client_secret"]
        else:
            self.client_id = client_id
            self.client_secret = client_secret
        self.square_client = Client()
        self.metrics_handler = MetricsHandler('oAuth')

    def get_token(self, code):
        """
        Makes a call to obtain the token.
        """
        response = self.square_client.o_auth.obtain_token(
            body={
                "client_id": self.client_id,
                "grant_type": "authorization_code",
                "client_secret": self.client_secret,
                "code": code,
            }
        )
        if response.is_success():
            self.metrics_handler.emit_metric(
                metric_name='oauth_authorization_code_success',
                value=1
            )
            return response.body
        try:
            error_detail = response.body["errors"][0]["detail"]
        except (KeyError, IndexError) as exc:
            self.metrics_handler.emit_metric(
                metric_name='oauth_authorization_code_failure',
                value=1,
                dimensions={'reason': 'unknown'}
            )
            raise self.UnknownAPIError(
                f"Request failed for an unknown reason: {response}"
            ) from exc
        if error_detail.startswith("Authorization code is expired."):
            self.metrics_handler.emit_metric(
                metric_name='oauth_authorization_code_failure',
                value=1,
                dimensions={'reason': 'expired_auth_code'}
            )
            raise self.ExpiredAuthCode()
        raise self.UnknownAPIError(
            f"Request failed for an unknown reason: {response}"
        )

    @staticmethod
    def get_refresh_after(expiry):
        """
        According to the Square guide, we should be refreshing the token
        before 7 days, so we'll set a refresh after timestamp at 6 days from
        now OR 2 days before the token expires if that is less. If the token
        expires within 2 days, the refresh after timestamp could be in the
        past.

        Tokens should last 30 days anyway, but we'll do this regardless.
        https://developer.squareup.com/docs/oauth-api/best-practices
        """
        if expiry.tzinfo:
            return min(
                expiry - timedelta(days=2),
                datetime.now(UTC) + timedelta(days=6)
            )
        else:
            return min(
                expiry - timedelta(days=2),
                datetime.now() + timedelta(days=6)
            )

