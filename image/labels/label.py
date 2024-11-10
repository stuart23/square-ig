from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader

from labels.qr_code import QRCode


def generate_label(item, html_output_file=None, debug=False):
    html = render_html(item, html_output_file, debug)
    screenshot = render_html_to_image(html)
    return screenshot


def render_html(item, html_output_file=None, debug=False):
    qr_code_base64 = QRCode(item.sku).base64_bw

    jinja_environment = Environment(
                loader=FileSystemLoader('assets')
            )
    template = jinja_environment.get_template("label_template.html")

    rendered_template = template.render(
        **item.__dict__,
        debug=debug,
        qr_code_base64=qr_code_base64.decode()
    )

    if html_output_file:
        with open(html_output_file, 'w') as fh:
            fh.write(rendered_template)
    
    return rendered_template


def render_html_to_image(html):
    with sync_playwright() as p:
        browser = p.webkit.launch()
        context = browser.new_context(viewport={"width": 500, "height": 300})
        page = context.new_page()
        page.set_content(html)
        screenshot = page.screenshot()
        browser.close()
    return screenshot

if __name__ == '__main__':
    from catalog import Item
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='Pilea abcdef',
        variation_str='4"',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    img = generate_label(item, html_output_file='rendered.html', debug=False)
    with open('output.png', 'wb') as fh:
        fh.write(img)
    img = generate_label(item, html_output_file='rendered_debug.html', debug=True)
    with open('output_debug.png', 'wb') as fh:
        fh.write(img)