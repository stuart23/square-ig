from git import Git, Repo
from os import getenv, chmod
from pathlib import Path
from shutil import rmtree
from boto3 import client as Boto3Client
from jinja2 import Environment, FileSystemLoader
from time import sleep

from utils import get_secret

GITHUB_KEY_ARN_ENV = "gh_key_arn"
KEY_FILE = Path('/tmp/id_rsa')
GIT_REPO_ENV = "instructions_git_repo"
REPO_DIR = '/tmp/repo'
TEMPLATE_DIR = Path(__file__).parent.resolve() / 'templates'


class DescriptionsGit(object):
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
        print(f'Repo {self.repo_url} successfully cloned to {self.repo_dir}')
        self.jinja_environment = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            extensions=['jinja2_time.TimeExtension']
        )


    def add_item(self, item, replace=False):
        '''
        Creates an item by templating the item.md file.

        If it already exists, then we wont overwrite it, just leave it as is and return False.

        If replace is true, it will delete the existing folder and re-template.
        '''
        template = self.jinja_environment.get_template("item.md")
        item_dir = self.repo_dir / "content" / item.sku_stem
        if item_dir.is_dir() and not replace:
            print(f'Skipping {item} as directory {item_dir} already exists')
            return False
        elif item_dir.is_dir():
            print(f'Deleting and recreating for {item} as directory {item_dir} already exists')
            rmtree(item_dir)
        item_dir.mkdir()
        output_file = item_dir / "index.md"

        content = template.render(**item.__dict__)
        with open(output_file, 'w') as fh:
            fh.write(content)
            print(f'Description for {item} written to {output_file}.')

        self.repo.index.add(output_file)

        return output_file
        

    @property
    def modified_files(self):
        '''
        Returns all the files that were modified in the git index.
        '''
        return [x.a_path for x in self.repo.index.diff("HEAD")]


    def commit(self):
        '''
        Commits the added files and pushes to GitHub if there are changes.
        '''
        if len(file_list) > 0:
            file_list = ', '.join(self.modified_files)
            print(f'Committing the following to git: {file_list}')
            self.repo.index.commit(f'Adding {file_list}')
            self.repo.remote('origin').push(env=self.git_environment)
        else:
            print(f'No changes, nothing to commit.')


    def __del__(self):
        '''
        Cleans up by removing the repo dir. If the object failed to init, the repo dir may not exist.
        Will try 5 times and 
        '''
        try:
            repo_dir = self.repo_dir
        except AttributeError:
            print('Repo dir was not created')
        else:
            for _ in range(5):
                rmtree(self.repo_dir)
                if self.repo_dir.is_dir():
                    print('Cleanup repo dir failed, retrying in 5 seconds.')
                    sleep(5)
                else:
                    print('Repo dir deleted.')
                    break
            else:
                print('Could not delete the repo dir.')