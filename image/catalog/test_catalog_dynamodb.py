from pytest import raises

from .catalog_dynamodb import get_item


def test_get_item_doesnt_exist():
    sku = 'poiuytrewq'
    with raises(ValueError) as excinfo:
        get_item(sku)
    assert str(excinfo.value) == 'Item not found'