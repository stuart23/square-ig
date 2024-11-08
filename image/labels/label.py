from labels.qr_code import QRCode
from PIL import Image, ImageOps, ImageFont, ImageDraw
from io import BytesIO
from pathlib import Path
from catalog import Item

LABEL_SIZE = (50, 30) # width x height
LABEL_DPMM = 20 # dots per millimeter
QR_SIZE = 72 # percentage of the height of the label
QR_PAD = 1 # millimeters from left and bottom for qr code start
pwd = Path(__file__).parent.resolve()
FLATTY_FONT = pwd / 'assets' / 'Flatty.otf'
TROPICA_FONT = pwd / 'assets' / 'Tropica Gardens Sans.otf'
PET_SAFE = pwd / 'assets' / 'pet_safe.png'
STORE_LOGO = pwd / 'assets' / 'store_logo.png'
TITLE_FONT_SIZE = 180
FORMAT = 'png'
real_padding = QR_PAD*LABEL_DPMM

def font_size(x):
    """
    Returns the font size for the level needed. Pass in the level:
    
    1: Title
    2: Subtitle
    3: Heading
    4: Text
    """
    return TITLE_FONT_SIZE/(1.2**(x-1))


def generate_label(item):
    width = LABEL_SIZE[0]*LABEL_DPMM
    height = LABEL_SIZE[1]*LABEL_DPMM
    label = Image.new('RGBA', (width, height), 'white')
    y_centerline = 9 * LABEL_DPMM
    insert_qr(label, item.sku, y_centerline=y_centerline)
    insert_logo(label, y_centerline=y_centerline)
    line_location = y_centerline * 2
    insert_vertical_bar(label, line_location, 20*LABEL_DPMM, 10)
    title_text_box = cropped_text(item.item_str, 3, TROPICA_FONT)

    text_left = line_location + 2*LABEL_DPMM
    label.paste(title_text_box, (text_left, 4*LABEL_DPMM))
    variation_text_box = cropped_text(item.variation_str, 5, TROPICA_FONT)
    label.paste(variation_text_box, (text_left, 11*LABEL_DPMM))

    text_center = (label.width - real_padding + text_left) //2
    price_text_box = cropped_text(f"${item.price/100}", 1, TROPICA_FONT)
    label.paste(price_text_box, (text_center - price_text_box.width//2, 16*LABEL_DPMM))
    if item.pet_safe:
        pet_safe_graphic = generate_pet_safe(label)
        label.paste(pet_safe_graphic, (text_center - pet_safe_graphic.width//2, label.height - real_padding - pet_safe_graphic.height))
    return label

def generate_label_bytes(item, filename):
    """
    Save the image to an in-memory file and return the bytes.
    """
    label = generate_label(item)
    in_mem_file = BytesIO()
    label.save(in_mem_file, format=FORMAT)
    in_mem_file.seek(0)
    in_mem_file.name = filename
    return in_mem_file

def generate_qr_leaf(label, sku):
    """
    Generates the leaf qr code and inserts it onto the label.
    """
    # PASTING THE QR
    qr_code = QRLeaf(sku).bw_qr
    rotated_qr = rotate_and_crop_image(qr_code, 45) # rotate by 45 degrees
    resized_qr = rotated_qr.resize((
        round(label.height*QR_SIZE/100*rotated_qr.width/rotated_qr.height), # multiplied by the aspect ratio because we are only trying to get the heights to match
        round(label.height*QR_SIZE/100)
    ))
    x_location = real_padding
    y_location = label.height - resized_qr.height - real_padding
    label.paste(resized_qr, (x_location, y_location))


def insert_qr(label, sku, y_centerline):
    """
    Generates the qr code and inserts it onto the label.
    """
    TEXT_FONT_SIZE = 11
    text = cropped_text('CARE INSTRUCTIONS', TEXT_FONT_SIZE, TROPICA_FONT)
    x_location = y_centerline - text.width // 2
    y_location = label.height - text.height - real_padding
    label.paste(text, (x_location, y_location))
    text = cropped_text('SCAN FOR', TEXT_FONT_SIZE, TROPICA_FONT)
    x_location = y_centerline - text.width // 2
    y_location = label.height - 2*text.height - real_padding - 10
    label.paste(text, (x_location, y_location))
    
    logo_size = 13 * LABEL_DPMM
    qr_code = QRCode(sku).bw_qr
    resized_qr_code = qr_code.resize((logo_size, logo_size))
    x_location = y_centerline - resized_qr_code.width // 2
    y_location = label.height - resized_qr_code.height - real_padding - 2*text.height - 20
    label.paste(resized_qr_code, (x_location, y_location))


def insert_vertical_bar(label, y_location, length, width):
    ImageDraw.Draw(label).line(
        (y_location, (label.height-length)//2, y_location, (label.height+length)//2),
        fill='BLACK',
        width=width
    )
    

def cropped_text(text, size, font):
    '''
    Returns an image with the text cropped to the right size.
    '''
    # Default size - may need to be adjusted?
    width = 5000
    height = 1000
    # Actual font size using the ratio formula
    actual_size = font_size(size)
    text_box = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(text_box)
    font = ImageFont.truetype(font, actual_size)
    draw.text((100,100), text, "black", font=font)
    bbox = ImageOps.invert(text_box.convert('RGB')).getbbox()
    cropped_text_box = text_box.crop(bbox)
    return cropped_text_box


def generate_pet_safe(label):
    '''
    Creates the pet_safe logo and puts it on the label.
    '''
    padding = 20 # distance between pet logo and text
    logo_size = 70 # size of the paw square
    # Import and resize the pet safe logo (paw)
    logo = Image.open(PET_SAFE)
    resized_logo = logo.resize((logo_size, logo_size))
    # Create a text box
    text_box = cropped_text('PET SAFE', 8, TROPICA_FONT)
    # Create the image with the logo and text
    height = max(text_box.height, resized_logo.height)
    width = text_box.width + resized_logo.width + padding
    pet_safe = Image.new('RGB', (width, height), 'white')

    pet_safe.paste(resized_logo,(0, int(height/2 - resized_logo.height/2)), resized_logo)
    pet_safe.paste(text_box, (resized_logo.width + padding, int(height/2 - text_box.height/2)), text_box)
    return pet_safe


def insert_logo(label, y_centerline):
    '''
    Creates the store logo and puts it on the label.
    '''
    logo_size = 13 * LABEL_DPMM # size of the paw square
    # Import and resize the store logo (paw)
    logo = Image.open(STORE_LOGO)
    resized_logo = logo.resize((logo_size, logo_size))
    bbox = ImageOps.invert(resized_logo.convert('RGB')).getbbox()
    cropped_logo = resized_logo.crop(bbox)
    x_location = y_centerline - cropped_logo.width // 2
    label.paste(cropped_logo,(x_location, real_padding))


def rotate_and_crop_image(image, angle):
    max_dimension = max(image.width, image.height)*3
    padded = Image.new(image.mode, (max_dimension, max_dimension), 'white')
    padded.paste(
        image,
        (
            round(max_dimension/2 - image.width/2),
            round(max_dimension/2 - image.height/2)
        )
    )
    rotated = padded.rotate(45,fillcolor='white')
    bbox = ImageOps.invert(rotated).getbbox()
    return rotated.crop(bbox)

if __name__ == '__main__':
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    generate_label(item).show()