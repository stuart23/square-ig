from PIL import ImageOps, ImageFilter, Image
from random import random
from pathlib import Path

from qrcode import QRCode, ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

from super_rounded_module_drawer import SuperRoundedModuleDrawer

MASK = Path(__file__).parent.resolve() / 'assets' / 'anthurium_mask.png'


class QRLeaf(object):
    light_green = (159, 255, 140)
    dark_green = (14, 66, 5)

    def __init__(self, code_text):
        self.qr = QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=0)
        self.qr.add_data(code_text)
        self.qr.make()
        self._random_pad(self.qr)

    @property
    def colour_qr(self):
        # Color Image
        qr_code_image = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SuperRoundedModuleDrawer(),
            eye_drawer=RoundedModuleDrawer(radius_ratio=0.75),
            color_mask=SolidFillColorMask(back_color=self.dark_green, front_color=self.light_green)
        )._img

        return self._mask_image_and_outline(qr_code_image, outline=2)


    @property
    def bw_qr(self):
        # BW Image
        qr_code_image = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SuperRoundedModuleDrawer(),
            eye_drawer=RoundedModuleDrawer(radius_ratio=0.75)
        )._img

        return self._mask_image_and_outline(qr_code_image, outline=2)

    @staticmethod
    def _random_pad(qr):
        '''
        Adds random noise around the qr code offset by the padding amount.
        '''
        padding = 1
        random_padding = 20
        new_size = qr.modules_count + 2 * random_padding

        output = [[False] * new_size for _ in range(new_size)]
        for row_index in range(new_size):
            for col_index in range(new_size):
                qr_row_coordinate, qr_column_coordinate = [row_index - random_padding - 1, col_index - random_padding - 1]
                if all([
                    qr_row_coordinate >= 0,
                    qr_row_coordinate < qr.modules_count,
                    qr_column_coordinate >= 0,
                    qr_column_coordinate < qr.modules_count
                ]):
                    output[row_index][col_index] = qr.modules[qr_row_coordinate][qr_column_coordinate]
                elif all([
                    qr_row_coordinate >= -padding,
                    qr_row_coordinate < qr.modules_count + padding,
                    qr_column_coordinate >= -padding,
                    qr_column_coordinate < qr.modules_count + padding
                ]):
                    output[row_index][col_index] = False
                else:
                    output[row_index][col_index] = random() < 0.5
        qr.modules = output
        qr.modules_count = new_size

    @staticmethod
    def _mask_image_and_outline(input_image, outline=True, outline_width=7, outline_color=(0,0,0)):
        blank = Image.new(
            input_image.mode, 
            input_image.size, 
            (255,255,255)
        ) 
        mask = Image.open(MASK).resize(input_image.size)
        masked_image = Image.composite(input_image,blank,mask)
        if outline:
            outline_image = mask.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(outline_width))
            blank_black = Image.new(
                masked_image.mode, 
                masked_image.size, 
                outline_color
            ) 
            return Image.composite(masked_image,blank_black,ImageOps.invert(outline_image))
        else:
            return masked_image