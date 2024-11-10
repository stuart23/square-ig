from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader


def generate_label(item, html_output_file=None):
    html = render_html(item, html_output_file)
    render_html_to_image(html)


def render_html(item, html_output_file=None):
    jinja_environment = Environment(
                loader=FileSystemLoader('assets')
            )
    template = jinja_environment.get_template("label_template.html")

    rendered_template = template.render(
        **item.__dict__
    )

    if html_output_file:
        with open('html_output_file', 'w') as fh:
            fh.write(rendered_template)
    
    return rendered_template


def render_html_to_image(html):
    with sync_playwright() as p:
        browser = p.webkit.launch()
        context = browser.new_context(viewport={"width": 500, "height": 300})
        page = context.new_page()
        page.set_content(html)
        page.screenshot(path='example.png')
        browser.close()

if __name__ == '__main__':
    from catalog import Item
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='Pilea',
        variation_str='4"',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    print(item.__dict__)
    generate_label(item, html_output_file='rendered.html')