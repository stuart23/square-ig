from .item import Item


def test_update_sku_ok():
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.update_sku() == False


def test_update_sku_no_url():
    item = Item(
        sku='abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.update_sku() == True
    assert item.sku == 'plantsoc.com/abcd1234'


def test_update_sku_no_sku():
    item = Item(
        sku='abcd1234',
        price=123,
        item_str='no_sku_123',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.update_sku() == False
    assert item.sku == 'abcd1234'


def test_update_sku_missing_sku():
    item = Item(
        sku=None,
        price=123,
        item_str='no_sku_123',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.update_sku() == True
    assert item.sku


def test_sku_stem_url_sku():
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.sku_stem == 'abcd1234'


def test_sku_stem_url_sku_not_formed():
    item = Item(
        sku='abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.sku_stem == 'abcd1234'


def test_sku_stem_url_sku_empty():
    item = Item(
        sku=None,
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.sku_stem == None


def test_serde():
    item = Item(
        sku=None,
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    item_dict = item.__dict__
    item_serde = Item(**item_dict)
    assert item == item_serde
