from PIL import ImageOps


def crop(image):
    '''
    Returns a cropped replica of the input image.
    '''
    bbox = ImageOps.invert(image.convert('RGB')).getbbox()
    return image.crop(bbox)