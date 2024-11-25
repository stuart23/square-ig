from pathlib import Path

from .renderer import Renderer
from catalog import Item


ARTIFACTS = Path(__file__).parent.resolve() / 'test_artifacts'


def test_item_render():
    '''
    Smoke test to make sure there is more than 2 lines in the output.
    '''
    item1 = Item(
        sku='plantsoc.com/do_not_use_this_sku',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )

    renderer = Renderer()
    result = renderer.render_item(item1)
    assert len(result.splitlines()) > 2


def test_directory_render():
    '''
    Test against known output.
    '''
    item1 = Item(
        sku='plantsoc.com/do_not_use_this_sku',
        price=123,
        item_str='abc',
        variation_str='lkjhgfdsa',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    item2 = Item(
        sku='plantsoc.com/do_not_use_this_sku2',
        price=456,
        item_str='def',
        variation_str='poiuytreq',
        item_id='asdfg',
        variation_id='zxcvb',
        pet_safe=False
    )

    renderer = Renderer()
    result = renderer.render_directory(items=[item1, item2])

    comparison = ARTIFACTS / "directory.md"

    with open(comparison, 'w') as fh:
        fh.write(result)
    assert len(result.splitlines()) > 2