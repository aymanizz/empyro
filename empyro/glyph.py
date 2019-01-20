"""Glyph support for terminal character creation.

defines Glyph class.
"""

from typing import NamedTuple, Union, Text

from . import color
from .color import Color
from .charcode import CharCode


_Glyph = NamedTuple('Glyph', [
    ('code', Union[Text, CharCode]),
    ('fg_color', Color),
    ('bg_color', Color),
])


class Glyph(_Glyph):
    """Represent a glyph

    code     -- a unicode code point or a character (str of length 1).
    fg_color -- the foreground color of the glyph.
    bg_color -- the background color of the glyph.
    """
    def __new__(cls, code: Union[Text, CharCode],
                 fg_color: Color = None,
                 bg_color: Color = None):
        if not isinstance(code, CharCode):
            code = CharCode(ord(code))
        fg_color = color.WHITE if fg_color is None else Color(*fg_color)
        bg_color = color.BLACK if bg_color is None else Color(*bg_color)
        return super().__new__(cls, code, fg_color, bg_color)


CLEAR = Glyph(CharCode.SPACE)
