from pytest import raises
from types import GeneratorType

from .catalog_dynamodb import get_item_by_sku, get_item_by_variation_id, get_needs_label_items, get_website_needs_update_items


def test_get_sku_doesnt_exist():
    sku = 'poiuytrewq'
    items = list(get_item_by_sku(sku))
    assert len(items) == 0


def test_get_variation_id_doesnt_exist():
    variation_id = 'poiuytrewq'
    with raises(ValueError) as excinfo:
        get_item_by_variation_id(variation_id)
    assert str(excinfo.value) == 'Item not found'


def test_get_website_needs_update_items():
    '''
    There may be no items that need a website, so we catch StopIteration.
    '''
    items = get_website_needs_update_items()
    assert isinstance(items, GeneratorType)
    try:
        next(items)
    except StopIteration:
        pass


def test_get_needs_label_items():
    '''
    There may be no items that need a label, so we catch StopIteration.
    '''
    items = get_needs_label_items()
    assert isinstance(items, GeneratorType)
    try:
        next(items)
    except StopIteration:
        pass