from pytest import raises

from .label import generate_label
from catalog import Item


def test_generate_label(tmp_path):
    '''
    Smoke test
    '''
    item = Item(
        sku='plantsoc.com/do_not_use_this_sku',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    label = generate_label(item)
    assert len(label) > 1