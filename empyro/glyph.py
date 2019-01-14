from typing import Union, Text

from . import color
from .color import Color
from .charcode import CharCode


class Glyph:
    def __init__(self, code: Union[Text, CharCode],
                 fg_color: Color = None,
                 bg_color: Color = None):
        if not isinstance(code, CharCode):
                code = CharCode(ord(code))
        self.code = code
        self.fg_color = color.WHITE if fg_color is None else Color(*fg_color)
        self.bg_color = color.BLACK if bg_color is None else Color(*bg_color)


CLEAR = Glyph(CharCode.SPACE)
