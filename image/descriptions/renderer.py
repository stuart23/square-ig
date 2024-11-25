from jinja2 import Environment, FileSystemLoader
from pathlib import Path


TEMPLATE_DIR = Path(__file__).parent.resolve() / 'templates'


class Renderer(object):
    def __init__(self):
        '''
        Sets up the jinja environment.
        '''
        self.jinja_environment = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            extensions=['jinja2_time.TimeExtension']
        )


    def render_item(self, item):
        '''
        Renders the template with the item details and returns the results.
        '''
        template = self.jinja_environment.get_template("item.md")
        content = template.render(item=item)
        return content


    def render_directory(self, items):
        '''
        Renders the directory. Takes a list of all the items and re
        '''
        template = self.jinja_environment.get_template("directory.md")
        content = template.render(items=items)
        return content
