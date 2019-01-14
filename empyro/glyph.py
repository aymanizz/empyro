"""Glyph support for terminal character creation.

defines Glyph class.
"""

from typing import Union, Text

from . import color
from .color import Color
from .charcode import CharCode


class Glyph:
    """Represent a glyph

    code     -- a unicode code point or a character (str of length 1).
    fg_color -- the foreground color of the glyph.
    bg_color -- the background color of the glyph.
    """
    def __init__(self, code: Union[Text, CharCode],
                 fg_color: Color = None,
                 bg_color: Color = None):
        if not isinstance(code, CharCode):
                code = CharCode(ord(code))
        self.code = code
        self.fg_color = color.WHITE if fg_color is None else Color(*fg_color)
        self.bg_color = color.BLACK if bg_color is None else Color(*bg_color)


CLEAR = Glyph(CharCode.SPACE)
