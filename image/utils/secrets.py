from boto3 import client as Boto3Client
from os import getenv

def get_secret(key):
    '''
    Returns a secret from secretsmanager given the env var key that contains the arn.
    '''
    arn = getenv(key)
    if not arn:
        raise KeyError('Key does not exist in env or is null')
    if not arn.startswith('arn'):
        raise KeyError('Key does not contain a valid secretsmanager arn')

    secretsmanager_client = Boto3Client('secretsmanager')
    return secretsmanager_client.get_secret_value(SecretId=arn)['SecretString']