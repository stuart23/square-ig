from pathlib import Path
from os import listdir, getenv

from .git_interface import InstructionsGit, REPO_DIR, GIT_REPO_ENV, GITHUB_KEY_ARN_ENV


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