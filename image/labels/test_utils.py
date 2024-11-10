from PIL import Image,  ImageDraw

from .utils import crop


def test_crop():
    '''
    Returns a cropped replica of the input image.

    Creates a blank canvas, draws a red square
    '''
    test_image = Image.new('RGB', (500, 500), 'white')
    draw = ImageDraw.Draw(test_image)
    draw.rectangle(((200, 200), (300, 300)), fill="red")
    cropped_image = crop(test_image)
    assert cropped_image.height == 101
    assert cropped_image.width == 101