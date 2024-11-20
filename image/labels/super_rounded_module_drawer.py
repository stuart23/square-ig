from typing import List
from PIL import Image, ImageDraw

from qrcode.image.styles.moduledrawers.pil import ANTIALIASING_FACTOR, RoundedModuleDrawer


def comparitor(is_active, active_list=[], inactive_list=[]):
    '''
    Takes 2 lists, an active and inactive list and only
    returns true if all the ones in the active list are
    active, and the ones in the inactive are inactive.
    '''
    active_values = [getattr(is_active, x) for x in active_list]
    inactive_values = [getattr(is_active, x) for x in inactive_list]
    if all(active_values) and not any(inactive_values):
        return True
    else:
        return False

class SuperRoundedModuleDrawer(RoundedModuleDrawer):
    '''
    Ref: https://github.com/lincolnloop/python-qrcode/blob/main/qrcode/image/styles/moduledrawers/pil.py#L97
    '''

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.SQUARE = Image.new(
            self.img.mode, (self.corner_width, self.corner_width), self.img.paint_color
        )
        self.setup_super_corners()
        self.setup_super_corners(inverse=True)
        self.setup_corners()
        self.setup_corners(inverse=True)


    def setup_super_corners(self, inverse=False):
        back_color = self.img.paint_color if inverse else self.img.color_mask.back_color
        front_color = self.img.color_mask.back_color if inverse else self.img.paint_color

        fake_width = self.img.box_size * ANTIALIASING_FACTOR
        radius = self.radius_ratio * fake_width
        diameter = radius * 2
        base = Image.new(
            self.img.mode, 
            (fake_width, fake_width), 
            back_color
        )  # make something 4x bigger for antialiasing
        base_draw = ImageDraw.Draw(base)
        base_draw.ellipse((0, 0, diameter, diameter), fill=front_color)
        if inverse:
            self.INVERSE_NW_SUPER_ROUND = base.resize(
                (self.img.box_size, self.img.box_size), Image.Resampling.LANCZOS
            )
            self.INVERSE_SW_SUPER_ROUND = self.INVERSE_NW_SUPER_ROUND.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            self.INVERSE_SE_SUPER_ROUND = self.INVERSE_NW_SUPER_ROUND.transpose(Image.Transpose.ROTATE_180)
            self.INVERSE_NE_SUPER_ROUND = self.INVERSE_NW_SUPER_ROUND.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        else:
            self.NW_SUPER_ROUND = base.resize(
                (self.img.box_size, self.img.box_size), Image.Resampling.LANCZOS
            )
            self.SW_SUPER_ROUND = self.NW_SUPER_ROUND.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            self.SE_SUPER_ROUND = self.NW_SUPER_ROUND.transpose(Image.Transpose.ROTATE_180)
            self.NE_SUPER_ROUND = self.NW_SUPER_ROUND.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    def setup_corners(self, inverse=False):
        back_color = self.img.paint_color if inverse else self.img.color_mask.back_color
        front_color = self.img.color_mask.back_color if inverse else self.img.paint_color

        fake_width = self.corner_width * ANTIALIASING_FACTOR
        radius = self.radius_ratio * fake_width
        diameter = radius * 2
        base = Image.new(
            self.img.mode, (fake_width, fake_width), back_color
        )  # make something 4x bigger for antialiasing
        base_draw = ImageDraw.Draw(base)
        base_draw.ellipse((0, 0, diameter, diameter), fill=front_color)
        base_draw.rectangle((radius, 0, fake_width, fake_width), fill=front_color)
        base_draw.rectangle((0, radius, fake_width, fake_width), fill=front_color)
        if inverse:
            self.INVERSE_NW_ROUND = base.resize(
                (self.corner_width, self.corner_width), Image.Resampling.LANCZOS
            )
            self.INVERSE_SW_ROUND = self.INVERSE_NW_ROUND.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            self.INVERSE_SE_ROUND = self.INVERSE_NW_ROUND.transpose(Image.Transpose.ROTATE_180)
            self.INVERSE_NE_ROUND = self.INVERSE_NW_ROUND.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        else:
            self.NW_ROUND = base.resize(
                (self.corner_width, self.corner_width), Image.Resampling.LANCZOS
            )
            self.SW_ROUND = self.NW_ROUND.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            self.SE_ROUND = self.NW_ROUND.transpose(Image.Transpose.ROTATE_180)
            self.NE_ROUND = self.NW_ROUND.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


    def drawrect(self, box: List[List[int]], is_active: "ActiveWithNeighbors"):
        if not is_active:
            self.drawWhiteModule(box, is_active)
        else:
            self.drawBlackModule(box, is_active)

    def drawBlackModule(self, box: List[List[int]], is_active: "ActiveWithNeighbors"):
        # find super rounded edges
        # nw_super_rounded
        if comparitor(is_active, active_list=['S', 'E'], inactive_list=['W', 'N', 'SW', 'NE']):
            self.img._img.paste(self.NW_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # ne_super_rounded
        if comparitor(is_active, active_list=['S', 'W'], inactive_list=['N', 'E', 'NW', 'SE']):
            self.img._img.paste(self.NE_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # se_super_rounded
        if comparitor(is_active, active_list=['N', 'W'], inactive_list=['S', 'E', 'NE', 'SW']):
            self.img._img.paste(self.SE_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # sw_super_rounded
        if comparitor(is_active, active_list=['E', 'N'], inactive_list=['S', 'W', 'NW', 'SE']):
            self.img._img.paste(self.SW_SUPER_ROUND, (box[0][0], box[0][1]))
            return

        # find rounded edges
        nw_rounded = not is_active.W and not is_active.N
        ne_rounded = not is_active.N and not is_active.E
        se_rounded = not is_active.E and not is_active.S
        sw_rounded = not is_active.S and not is_active.W

        nw = self.NW_ROUND if nw_rounded else self.SQUARE
        ne = self.NE_ROUND if ne_rounded else self.SQUARE
        se = self.SE_ROUND if se_rounded else self.SQUARE
        sw = self.SW_ROUND if sw_rounded else self.SQUARE
        self.img._img.paste(nw, (box[0][0], box[0][1]))
        self.img._img.paste(ne, (box[0][0] + self.corner_width, box[0][1]))
        self.img._img.paste(
            se, (box[0][0] + self.corner_width, box[0][1] + self.corner_width)
        )
        self.img._img.paste(sw, (box[0][0], box[0][1] + self.corner_width))

    def drawWhiteModule(self, box: List[List[int]], is_active: "ActiveWithNeighbors"):
        # find super rounded edges
        # nw_super_rounded
        if comparitor(is_active, active_list=['S', 'E', 'SE', 'SW', 'NE'], inactive_list=['N', 'W']):
            self.img._img.paste(self.INVERSE_SE_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # ne_super_rounded
        if comparitor(is_active, active_list=['S', 'W', 'SW', 'NW', 'SE'], inactive_list=['N', 'E']):
            self.img._img.paste(self.INVERSE_SW_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # se_super_rounded
        if comparitor(is_active, active_list=['N', 'W', 'NW', 'NE', 'SW'], inactive_list=['S', 'E']):
            self.img._img.paste(self.INVERSE_NW_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # sw_super_rounded
        if comparitor(is_active, active_list=['E', 'N', 'NE', 'NW', 'SE'], inactive_list=['S', 'W']):
            self.img._img.paste(self.INVERSE_NE_SUPER_ROUND, (box[0][0], box[0][1]))
            return
        # # find rounded edges
        # nw_rounded
        if comparitor(is_active, active_list=['N', 'NW', 'W']):
            self.img._img.paste(self.INVERSE_NW_ROUND, (box[0][0], box[0][1]))
        # ne_rounded
        if comparitor(is_active, active_list=['N', 'NE', 'E']):
            self.img._img.paste(self.INVERSE_NE_ROUND, (box[0][0] + self.corner_width, box[0][1]))
        # se_rounded
        if comparitor(is_active, active_list=['S', 'SE', 'E']):
            self.img._img.paste(self.INVERSE_SE_ROUND, (box[0][0] + self.corner_width, box[0][1] + self.corner_width))
        # sw_rounded
        if comparitor(is_active, active_list=['S', 'SW', 'W']):
            self.img._img.paste(self.INVERSE_SW_ROUND, (box[0][0], box[0][1] + self.corner_width))