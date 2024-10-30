from pathlib import Path
from os import listdir, getenv

from .git_interface import InstructionsGit, REPO_DIR, GIT_REPO_ENV, GITHUB_KEY_ARN_ENV
from catalog import Item


def test_gh_repo_env_exists():
    assert getenv(GIT_REPO_ENV)


def test_gh_key_env_exists():
    assert getenv(GITHUB_KEY_ARN_ENV)


def test_git_interface_clone():
    '''
    Test to see that it has cloned the repo.
    '''
    repo_dir = Path(REPO_DIR)
    assert not repo_dir.is_dir(), 'Directory already exists.'

    instructions = InstructionsGit()
    assert instructions.repo_dir.is_dir(), 'Directory not created.'
    assert len(listdir(instructions.repo_dir)) > 0, 'No files in the directory.'


def test_git_interface_add_item():
    '''
    Test templating.
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
    item2 = Item(
        sku='plantsoc.com/do_not_use_this_sku2',
        price=456,
        item_str='def',
        variation_str='def',
        item_id='asdfg',
        variation_id='zxcvb',
        pet_safe=False
    )

    instructions = InstructionsGit()
    instructions.add_item(item1)
    item1_instructions_dir = instructions.repo_dir / "content" / "abcd1234"
    assert item1_instructions_dir.is_dir(), 'Directory not created.'
    item1_readme = item1_instructions_dir / "index.md"
    assert item1_readme.is_file(), 'Readme not created.'

    instructions.add_item(item2)
    item2_instructions_dir = instructions.repo_dir / "content" / "efgh5678"
    assert item2_instructions_dir.is_dir(), 'Directory not created.'
    item2_readme = item2_instructions_dir / "index.md"
    assert item2_readme.is_file(), 'Readme not created.'

    assert instructions.added_files == ['content/do_not_use_this_sku/index.md', 'content/do_not_use_this_sku2/index.md']