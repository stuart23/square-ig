from .label import generate_label, generate_label_bytes
from catalog import Item


def test_generate_label(tmp_path):
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
    label_file = tmp_path / 'label.png'
    label.save(label_file)
    assert label_file.is_file()


def test_generate_label_bytes(tmp_path):
    item = Item(
        sku='plantsoc.com/do_not_use_this_sku',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    filename = 'Pilea-4.png'
    label_bytes = generate_label_bytes(item, filename)
    assert label_bytes
    assert label_bytes.name == filename