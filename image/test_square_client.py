from types import GeneratorType
from uuid import uuid4
from os import getenv
from pytest import raises

from square_client import SquareClient, SQUARE_TOKEN_ARN_ENV
from catalog import Item


def test_square_env_exists():
    assert getenv(SQUARE_TOKEN_ARN_ENV)


def test_get_client():
    # TODO: Can we test that it is successful or just that it doesn't raise any exception?
    client = SquareClient._get_square_client()


def test__get_records_from_square_items():
    '''
    Test the square interface to get all items.
    '''
    client = SquareClient()
    items = client._get_records_from_square()
    assert isinstance(items, GeneratorType)
    item_0 = next(items)
    assert isinstance(item_0, dict)
    assert item_0['type'] == 'ITEM'
    item_1 = next(items)
    assert isinstance(item_1, dict)
    assert item_1['type'] == 'ITEM'
    item_2 = next(items)
    assert isinstance(item_2, dict)
    assert item_2['type'] == 'ITEM'


def test__get_records_from_square_categories():
    '''
    Test the square interface to get all categories.
    '''
    client = SquareClient()
    items = client._get_records_from_square(object_type='CATEGORY')
    assert isinstance(items, GeneratorType)
    item_0 = next(items)
    assert isinstance(item_0, dict)
    assert item_0['type'] == 'CATEGORY'
    item_1 = next(items)
    assert isinstance(item_1, dict)
    assert item_1['type'] == 'CATEGORY'
    item_2 = next(items)
    assert isinstance(item_2, dict)
    assert item_2['type'] == 'CATEGORY'


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


def test_categories():
    client = SquareClient()
    categories = client.categories
    assert len(categories) > 0
    assert categories[0]['type'] == 'CATEGORY'


def test_get_matching_category():
    client = SquareClient()
    match = client._get_matching_category('ODMHZODS4WHR7NV3UAVE43PB')
    assert match['id'] == 'ODMHZODS4WHR7NV3UAVE43PB'
    assert match['category_data']['name'] == 'Pins'


def test_get_matching_category_missing():
    client = SquareClient()
    with raises(ValueError) as excinfo:
        client._get_matching_category('ASDFGHQWERTY')
    assert str(excinfo.value) == 'No matching category with ID ASDFGHQWERTY'


def test_get_categories():
    '''
    Assume `ODMHZODS4WHR7NV3UAVE43PB` maps to ``
    if this starts failing, check that the mapping is still correct in square.
    '''
    client = SquareClient()
    item_data = {'categories': [{'id': 'ODMHZODS4WHR7NV3UAVE43PB', 'ordinal': -2251731094208512},]}
    categories = client.get_categories(item_data)
    assert categories == [{'id': 'ODMHZODS4WHR7NV3UAVE43PB', 'name': 'Pins'}]