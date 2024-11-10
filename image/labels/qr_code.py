from PIL import ImageOps, ImageFilter, Image
from random import random
from pathlib import Path
from base64 import b64encode
from io import BytesIO

from qrcode import QRCode as _QRCode, ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

from labels.super_rounded_module_drawer import SuperRoundedModuleDrawer

MASK = Path(__file__).parent.resolve() / 'assets' / 'anthurium_mask.png'


class QRCode(object):
    def __init__(self, code_text):
        self.qr = _QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=0)
        self.qr.add_data(code_text)
        self.qr.make()

    @property
    def colour_qr(self):
        # Color Image
        qr_code_image = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SuperRoundedModuleDrawer(),
            eye_drawer=RoundedModuleDrawer(radius_ratio=0.75),
        )._img

        return qr_code_image


    @property
    def bw_qr(self):
        # BW Image
        qr_code_image = self.qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SuperRoundedModuleDrawer(),
            eye_drawer=RoundedModuleDrawer(radius_ratio=0.75)
        )._img

        return qr_code_image

    @property
    def base64_bw(self):
        qr_code = self.bw_qr
        buffered = BytesIO()
        qr_code.save(buffered, format="png")
        return b64encode(buffered.getvalue())

if __name__ == '__main__':
    QRCode('plantsoc.com/abcdefgh').bw_qr.save('test.png')