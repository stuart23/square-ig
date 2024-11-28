from types import GeneratorType
from uuid import uuid4
from os import getenv

from square_client import SquareClient, SQUARE_TOKEN_ARN_ENV
from catalog import Item


def test_square_env_exists():
    assert getenv(SQUARE_TOKEN_ARN_ENV)


def test_get_client():
    # TODO: Can we test that it is successful or just that it doesn't raise any exception?
    client = SquareClient._get_square_client()


def test__get_all_catalog_items():
    '''
    Test the square interface.
    '''
    client = SquareClient()
    items = client._get_all_catalog_items()
    assert isinstance(items, GeneratorType)
    item_0 = next(items)
    assert isinstance(item_0, dict)
    item_1 = next(items)
    assert isinstance(item_1, dict)
    item_2 = next(items)
    assert isinstance(item_2, dict)


def test_get_catalog_items():
    '''
    Test the Items generator.
    '''
    client = SquareClient()
    items = client.get_catalog_items()
    assert isinstance(items, GeneratorType)
    item_0 = next(items)
    assert isinstance(item_0, Item)
    item_1 = next(items)
    assert isinstance(item_1, Item)
    item_2 = next(items)
    assert isinstance(item_2, Item)


def test_upsert_catalog_object():
    sku = str(uuid4()).replace('-', '')[:8]
    client = SquareClient()
    for item in client.get_catalog_items():
        if item.item_str.startswith('no_sku'):
            item.sku = sku
            client.patch_objects_sku(items=[item])
            break
    else:
        raise Exception('No no_sku items exist')
    for item in client.get_catalog_items():
        if item.item_str.startswith('no_sku'):
            assert item.sku == sku