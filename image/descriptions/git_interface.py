from git import Git, Repo
from os import getenv, chmod
from pathlib import Path
from shutil import rmtree
from boto3 import client as Boto3Client
from jinja2 import Environment, FileSystemLoader

from utils import get_secret

GITHUB_KEY_ARN_ENV = "gh_key_arn"
KEY_FILE = Path('/tmp/id_rsa')
GIT_REPO_ENV = "instructions_git_repo"
REPO_DIR = '/tmp/repo'
TEMPLATE_DIR = Path(__file__).parent.resolve() / 'templates'


class InstructionsGit(object):
    def __init__(self, repo_dir=REPO_DIR):
        '''
        Writes the key from secrets manager if it doesn't already exist.
        '''
        self.repo_url = getenv(GIT_REPO_ENV)

        if not KEY_FILE.is_file():
            key = get_secret(GITHUB_KEY_ARN_ENV)
            with open(KEY_FILE, 'w') as key_file:
                key_file.write(key)
            chmod(KEY_FILE, 0o600)
    
        self.git_environment = {'GIT_SSH_COMMAND': f'ssh -o StrictHostKeyChecking=no -i {KEY_FILE}'}
        self.repo_dir = Path(REPO_DIR)
        self.repo_dir.mkdir()

        self.repo = Repo.clone_from(self.repo_url, self.repo_dir, env=self.git_environment)

        self.jinja_environment = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            extensions=['jinja2_time.TimeExtension']
        )


    def add_item(self, item_details):
        '''
        Creates an item by templating the item.md file.
        '''
        template = self.jinja_environment.get_template("item.md")
        url = item_details["sku"].replace("plantsoc.com/", "")
        item_dir = self.repo_dir / url
        item_dir.mkdir()

        content = template.render(**item_details)
        with open(item_dir / 'index.md', 'w') as fh:
            fh.write(content)

        self.repo.index.add(Path(url) / 'index.md')
        

    def commit(self):
        '''
        Commits the added files and pushes to GitHub.
        '''
        message = 'Adding ' + ', '.join([x[0] for x in self.repo.index.entries.keys()])
        self.repo.index.commit(message)
        self.repo.remote('origin').push(env=self.git_environment)

    def __del__(self):
        '''
        Cleans up by removing the repo dir. If the object failed to init, the repo dir may not exist
        '''
        try:
            repo_dir = self.repo_dir
        except AttributeError:
            print('Repo dir was not created')
        else:
            rmtree(self.repo_dir)