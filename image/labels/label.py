from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader
from base64 import b64encode
from time import sleep

from labels.qr_code import QRCode


def generate_label(item, html_output_file=None, image_output_file=None, debug=False):
    statics = load_statics()
    html = render_html(item, statics, html_output_file=None, debug=debug)
    
    if html_output_file:
        with open(html_output_file, 'w') as fh:
            fh.write(html)

    screenshot = render_html_to_image(html)
            
    if image_output_file:
        with open(image_output_file, 'wb') as fh:
            fh.write(screenshot)
            
    return screenshot


def load_statics():
    '''
    Loads the static files that are in the template and
    returns them as a dict of base64 encoded strings
    '''
    from labels import assets_dir

    tokens = {}
    with open(assets_dir / "Flatty.otf", "rb") as fh:
        tokens['Flatty'] = b64encode(fh.read()).decode()

    with open(assets_dir / "Tropica Gardens Sans.otf", "rb") as fh:
        tokens['TropicaGardensSans'] = b64encode(fh.read()).decode()

    with open(assets_dir / "store_logo.png", "rb") as fh:
        tokens['store_logo'] = b64encode(fh.read()).decode()

    with open(assets_dir / "pet_safe.png", "rb") as fh:
        tokens['pet_safe_img'] = b64encode(fh.read()).decode()

    return tokens

def render_html(item, statics, html_output_file=None, debug=False):
    print('Templating HTML')
    from labels import assets_dir
    
    qr_code_base64 = QRCode(item.sku).base64_bw

    jinja_environment = Environment(
                loader=FileSystemLoader(assets_dir)
            )
    template = jinja_environment.get_template("label_template.html")

    rendered_template = template.render(
        **item.__dict__,
        **statics,
        debug=debug,
        qr_code_base64=qr_code_base64.decode()
    )

    if html_output_file:
        with open(html_output_file, 'w') as fh:
            fh.write(rendered_template)
    print('Templating HTML finished')
    
    return rendered_template


def render_html_to_image(html):
    print('Rendering HTML')
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--single-process"],
        )
        context = browser.new_context(viewport={"width": 500, "height": 300})
        page = context.new_page()
        page.set_content(html)
        from time import sleep
        sleep(1)
        page.wait_for_function("ready")
        screenshot = page.screenshot()
        browser.close()
    print('Rendering HTML finished')
    return screenshot

if __name__ == '__main__':
    from catalog import Item
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='Worlds best plant killer sticker',
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