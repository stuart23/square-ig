from pytest import raises
from os import environ
from botocore.exceptions import ClientError

from . import get_secret

'''
We don't have a test for a valid secret because we don't necessarily have a valid secret available.
'''

def test_get_secret_arn_missing():
    with raises(KeyError) as excinfo:
        secret_arn = get_secret('asdf1234')
    assert 'Key does not exist in env or is null' in str(excinfo.value)


def test_get_secret_arn_invalid():
    environ['MY_KEY'] = 'qwerty'
    with raises(KeyError) as excinfo:
        secret_arn = get_secret('MY_KEY')
    assert 'Key does not contain a valid secretsmanager arn' in str(excinfo.value)
    

def test_get_secret_arn_fake():
    environ['MY_KEY'] = 'arn:aws:secretsmanager:'
    with raises(ClientError) as excinfo:
        secret_arn = get_secret('MY_KEY')
    assert 'Invalid name' in str(excinfo.value)
    