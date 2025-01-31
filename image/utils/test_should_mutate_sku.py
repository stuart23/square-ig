from . import should_mutate_sku
from os import environ


def test_no_envvar():
    merchant_details = {'id': 'abcd'}
    response = should_mutate_sku(merchant_details)
    assert response == False


def test_no_key():
    environ['env'] = 'dev'
    merchant_details = {'id': 'abcd'}
    response = should_mutate_sku(merchant_details)
    assert response == False


def test_woth_key_false():
    environ['env'] = 'dev'
    merchant_details = {'id': 'abcd', 'dev_update_skus': False}
    response = should_mutate_sku(merchant_details)
    assert response == False


def test_woth_key_true():
    environ['env'] = 'dev'
    merchant_details = {'id': 'abcd', 'dev_update_skus': True}
    response = should_mutate_sku(merchant_details)
    assert response == True

