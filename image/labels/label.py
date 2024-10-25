from .qr_leaf import QRLeaf
from PIL import Image, ImageOps, ImageFont, ImageDraw
from io import BytesIO

LABEL_SIZE = (50, 30) # width x height
LABEL_DPMM = 20 # dots per millimeter
QR_SIZE = 75 # percentage of the height of the label
QR_HORIZONTAL_PAD = 1 # millimeters from left for qr code start
FLATTY_FONT = "assets/Flatty.otf"
TROPICA_FONT = "assets/Tropica Gardens Sans.otf"
TITLE_FONT_SIZE = 150

def font_size(x):
    """
    Returns the font size for the level needed. Pass in the level:
    
    1: Title
    2: Subtitle
    3: Heading
    4: Text
    """
    return TITLE_FONT_SIZE/(1.2**(x-1))


def generate_label(sku, title, variation, price, pet_safe):
    width = LABEL_SIZE[0]*LABEL_DPMM
    height = LABEL_SIZE[1]*LABEL_DPMM
    label = Image.new('RGBA', (width, height), 'white')
    generate_qr(label, sku)
    title_text_box = cropped_text(title, 1, FLATTY_FONT)
    label.paste(title_text_box, (520, 60))
    variation_text_box = cropped_text(variation, 2, FLATTY_FONT)
    label.paste(variation_text_box, (520, 200))
    price_text_box = cropped_text(f"${price}", 2, FLATTY_FONT)
    label.paste(price_text_box, (950-price_text_box.width, 320))
    if pet_safe:
        pet_safe = generate_pet_safe(label)
        label.paste(pet_safe, (520, 450))
    return label

def generate_label_bytes(*args, **kwargs):
    """
    Save the image to an in-memory file and return the bytes.
    """
    label = generate_label(*args, **kwargs)
    in_mem_file = BytesIO()
    label.save(in_mem_file, format=FORMAT)
    in_mem_file.seek(0)
    return in_mem_file

def generate_qr(label, sku):
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
    x_location = QR_HORIZONTAL_PAD*LABEL_DPMM
    y_location = round((label.height - resized_qr.height)/2)
    label.paste(resized_qr, (x_location, y_location))

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
    draw.text((0,0), text, "black", font=font)
    bbox = ImageOps.invert(text_box.convert('RGB')).getbbox()
    cropped_text_box = text_box.crop(bbox)
    return cropped_text_box


def generate_pet_safe(label):
    '''
    Creates the pet_safe logo and puts it on the label.
    '''
    padding = 20 # distance between pet logo and text
    logo_size = 80 # size of the paw square
    # Import and resize the pet safe logo (paw)
    logo = Image.open("assets/pet_safe.png")
    resized_logo = logo.resize((logo_size, logo_size))
    # Create a text box
    text_box = cropped_text('PET SAFE', 5, TROPICA_FONT)
    # Create the image with the logo and text
    height = max(text_box.height, resized_logo.height)
    width = text_box.width + resized_logo.width + padding
    pet_safe = Image.new('RGB', (width, height), 'white')

    pet_safe.paste(resized_logo,(0, int(height/2 - resized_logo.height/2)), resized_logo)
    pet_safe.paste(text_box, (resized_logo.width + padding, int(height/2 - text_box.height/2)), text_box)
    return pet_safe

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
    generate_label(
        sku='plantsoc.io/abcd1234',
        title='Pilea',
        variation='4"',
        price=123.45,
        pet_safe=True
    ).show()