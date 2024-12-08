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
        variation_str='abcdef',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.update_sku() == True
    assert item.sku == 'plantsoc.com/asdfg'


def test_validate_sku_valid():
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abcd1234',
        variation_str='asdfg',
        item_id='qwerty',
        variation_id='poiuytrewq',
        pet_safe=True
    )
    assert item.validate_sku() == True
    assert item.sku == 'plantsoc.com/abcd1234'


def test_validate_sku_too_long():
    item = Item(
        sku='plantsoc.com/abcd12345678',
        price=123,
        item_str='abcd1234',
        variation_str='asdfg',
        item_id='qwerty',
        variation_id='poiuytrewq',
        pet_safe=True
    )
    assert item.validate_sku() == False
    assert item.sku == 'plantsoc.com/poiuytre'


def test_validate_sku_invalid_chars():
    item = Item(
        sku='plantsoc.com/abc. 12',
        price=123,
        item_str='abcd1234',
        variation_str='asdfg',
        item_id='qwerty',
        variation_id='poiuytrewq',
        pet_safe=True
    )
    assert item.validate_sku() == False
    assert item.sku == 'plantsoc.com/poiuytre'


def test_item_categories():
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True,
        categories=['my_category']
    )
    assert len(item.categories) == 1
    assert item.categories[0] == 'my_category'


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


def test_square_link():
    item = Item(
        sku=None,
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    assert item.square_link == 'https://app.squareup.com/dashboard/items/library/qwerty'


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


def test_fromSquare():
    item_str = 'Pink Princess Pin'
    variation_details = {
        'id': 'HFS35APE35PLE74GAKFGCL3M',
        'item_variation_data': {
            'item_id': 'N3PPIULUZSBLXA3AESGITJ7T',
            'name': 'Regular',
            'price_money': {'amount': 399, 'currency': 'USD'},
            'sku': 'plantsoc.com/542513F',
        },
    }

    item = Item.fromSquareDetails(item_str, variation_details)
    assert item.sku == 'plantsoc.com/542513F'
    assert item.price == 399
    assert item.item_str == 'Pink Princess Pin'
    assert item.variation_str == 'Regular'
    assert item.item_id == 'N3PPIULUZSBLXA3AESGITJ7T'
    assert item.variation_id == 'HFS35APE35PLE74GAKFGCL3M'
    # Should default to false
    assert item.pet_safe == False


def test_fromSquare_with_petsafe_true():
    item_str = 'Pink Princess Pin'
    variation_details = {
        'id': 'HFS35APE35PLE74GAKFGCL3M',
        'item_variation_data': {
            'item_id': 'N3PPIULUZSBLXA3AESGITJ7T',
            'name': 'Regular',
            'price_money': {'amount': 399, 'currency': 'USD'},
            'sku': 'plantsoc.com/542513F',
        },
    }
    custom_attribute_values = {
        'Square:93cd2840-5cff-4bea-8b7d-c83434f6f6c0': {
            'name': 'Pet Safe',
            'custom_attribute_definition_id': 'E7NHJOCYVPOYBVGARDS73ASE',
            'type': 'BOOLEAN',
            'boolean_value': True,
            'key': 'Square:93cd2840-5cff-4bea-8b7d-c83434f6f6c0'
        }
    }

    item = Item.fromSquareDetails(item_str, variation_details, custom_attribute_values)
    assert item.sku == 'plantsoc.com/542513F'
    assert item.price == 399
    assert item.item_str == 'Pink Princess Pin'
    assert item.variation_str == 'Regular'
    assert item.item_id == 'N3PPIULUZSBLXA3AESGITJ7T'
    assert item.variation_id == 'HFS35APE35PLE74GAKFGCL3M'
    assert item.pet_safe == True


def test_fromSquare_with_petsafe_false():
    item_str = 'Pink Princess Pin'
    variation_details = {
        'id': 'HFS35APE35PLE74GAKFGCL3M',
        'item_variation_data': {
            'item_id': 'N3PPIULUZSBLXA3AESGITJ7T',
            'name': 'Regular',
            'price_money': {'amount': 399, 'currency': 'USD'},
            'sku': 'plantsoc.com/542513F',
        },
    }
    custom_attribute_values = {
        'Square:93cd2840-5cff-4bea-8b7d-c83434f6f6c0': {
            'name': 'Pet Safe',
            'custom_attribute_definition_id': 'E7NHJOCYVPOYBVGARDS73ASE',
            'type': 'BOOLEAN',
            'boolean_value': False,
            'key': 'Square:93cd2840-5cff-4bea-8b7d-c83434f6f6c0'
        }
    }

    item = Item.fromSquareDetails(item_str, variation_details, custom_attribute_values)
    assert item.sku == 'plantsoc.com/542513F'
    assert item.price == 399
    assert item.item_str == 'Pink Princess Pin'
    assert item.variation_str == 'Regular'
    assert item.item_id == 'N3PPIULUZSBLXA3AESGITJ7T'
    assert item.variation_id == 'HFS35APE35PLE74GAKFGCL3M'
    assert item.pet_safe == False


def test_fromSquare_with_categories():
    item_str = 'Pink Princess Pin'
    variation_details = {
        'id': 'HFS35APE35PLE74GAKFGCL3M',
        'item_variation_data': {
            'item_id': 'N3PPIULUZSBLXA3AESGITJ7T',
            'name': 'Regular',
            'price_money': {'amount': 399, 'currency': 'USD'},
            'sku': 'plantsoc.com/542513F',
        },
    }

    item = Item.fromSquareDetails(item_str, variation_details, categories=['my_category_1', 'my_category_2'])
    assert len(item.categories) == 2
    assert item.categories[0] == 'my_category_1'
    assert item.categories[1] == 'my_category_2'