"""Provide the virtual terminal base class used for emulation.

defines the following classes:
    Terminal    -- base class for terminals.
    Subterminal -- a subterminal of a parent/root terminal.
"""

from abc import ABC, abstractmethod
from typing import Union, Text

from . import color
from . import glyph
from .color import Color
from .glyph import Glyph
from .charcode import CharCode
from .coord import Point, Size, Rect


class Terminal(ABC):
    """Terminal base class, represent a virtual terminal window.
    Only requires the implementation of the `draw_glyph` method.

    properties:
        rect -- the rectangle that defines the shape of the terminal,
                mainly its width and height.
                terminal instances always have x and y set to 0.
        fg_color -- default foreground color.
        bg_color -- default background color.
    """
    def __init__(self, size: Size):
        self.bg_color = color.BLACK
        self.fg_color = color.WHITE
        self.rect = Rect(0, 0, *size)

    def color(self, fg: Color, bg: Color):
        """Set the default foreground and background colors."""
        self.fg_color, self.bg_color = fg, bg
        return self

    def write_at(self, char: Union[Text, CharCode], at: Point,
                 fg_color: Color = None, bg_color: Color = None):
        """Write a character at the specified position.

        If no colors are specified, the default colors are used.
        """
        if fg_color is None:
            fg_color = self.fg_color
        if bg_color is None:
            bg_color = self.bg_color
        self.draw_glyph(
            at, Glyph(char, self.fg_color, self.bg_color))
        return self

    def fill(self, bg: Color, window: Rect):
        """Fill a portion of the terminal with the specified color.
        """
        if window not in self.rect:
            raise ValueError('window out of bounds')

        _glyph = Glyph(CharCode.SPACE, None, bg)
        for _y in range(window[1], window[3]):
            for _x in range(window[0], window[2]):
                self.draw_glyph(Point(_x, _y), _glyph)
        return self

    def clear(self, window: Rect = None):
        """Clear the terminal using the default background color.

        Optionally, a `window` argument can be passed to clear just
        that portion.
        """
        if window not in self.rect:
            raise ValueError('window out of bounds')

        window = self.rect if window is None else window
        self.fill(self.bg_color, window)
        return self

    def view(self, window: Rect):
        """Return a sub view into the terminal, see `Subterminal`.
        """
        return Subterminal(self, window)

    @abstractmethod
    def draw_glyph(self, glyph_: Glyph, at: Point):
        pass


class Subterminal(Terminal):
    """Provide a way to treat a portion of the root terminal as a
    standalone terminal. Implements `Terminal` ABC.

    additional properties:
        root -- the root/parent terminal.

    Any writes to the subterminal are writes to the root terminal.
    """
    def __init__(self, root: Terminal, window: Rect):
        if window not in root._rect:
            raise ValueError('window out of bounds')
        super().__init__((window[2], window[3]))
        self.rect = Rect(*window)
        self._root = root

    @property
    def root(self):
        return self._root

    # override to eliminate nested subterminals
    def view(self, window: Rect):
        if window not in self._view_window:
            raise ValueError('window out of bounds')
        return Subterminal(self._root, window)

    def draw_glyph(self, glyph_: Glyph, at: Point):
        point = Point(self._view_window.x + at[0],
                      self._view_window.y + at[1])
        self._root.draw_glyph(point, glyph_)
