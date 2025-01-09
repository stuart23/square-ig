from datetime import datetime, timedelta
from square.client import Client
from json import loads

from utils import get_secret

SQUARE_QR_CODES_CREDENTIALS_ARN = 'square_qr_codes_credentials_arn'



class TokenServices:
    class ExpiredAuthCode(Exception):
    """Exception raised if Square rejects the request because the Auth Code has expired."""
    def __str__(self):
        return "Authorization Code has expired"


    def __init__(self, client_id=None, client_secret=None):
        '''
        Pass in BOTH square application credentials otherwise they will be retrieved
        from the secret referenced in the envvar set above in 
        SQUARE_QR_CODES_CREDENTIALS_ARN.
        '''
        if not client_id and not client_secret:
            square_application_credentials = loads(get_secret(SQUARE_QR_CODES_CREDENTIALS_ARN))
            self.client_id = square_application_credentials['client_id']
            self.client_secret = square_application_credentials['client_secret']
        else:
            self.client_id = client_id
            self.client_secret = client_secret
        self.square_client = Client()


    def get_token(self, code):
        '''
        Makes a call to obtain the token.
        '''
        response = self.square_client.o_auth.obtain_token(
            body={
                'client_id': self.client_id,
                'grant_type': 'authorization_code',
                'client_secret': self.client_secret,
                'code': code
            }
        )
        if response.is_success():
            return response.body
        else:
            try:
                error_detail = response['errors'][0]['detail']
            except KeyError, IndexError:
                raise Exception(f'Request failed for an unknown reason: {response}')
            if error_detail.startswith('Authorization code is expired.'):
                raise ExpiredAuthCode()

    @staticmethod
    def get_refresh_after(expiry):
        '''
        According to the Square guide, we should be refreshing the token before 7 days,
        so we'll set a refresh after timestamp at 6 days from now OR 2 days before the
        token expires if that is less. If the token expires within 2 days, the refresh
        after timestamp could be in the past.

        Tokens should last 30 days anyway, but we'll do this regardless.
        https://developer.squareup.com/docs/oauth-api/best-practices
        '''
        return min(expiry - timedelta(days=2), datetime.now() + timedelta(days=6))