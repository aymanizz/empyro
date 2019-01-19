"""Provide the virtual terminal base class used for emulation.

defines the following classes:
    Terminal    -- base class for terminals.
    Subterminal -- a subterminal of a parent/root terminal.
"""

from abc import ABC, abstractmethod
from typing import Union, Text, List

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
        size -- the rectangle that defines the size of the terminal,
                mainly its width and height.
                terminal instances always have x and y set to 0
                and defaults to a size of 80x24.
        fg_color -- default foreground color.
        bg_color -- default background color.
    """

    def __init__(self, size: Size = None):
        self.bg_color = color.BLACK
        self.fg_color = color.WHITE
        size = (80, 24) if size is None else size
        self.size = Rect(0, 0, *size)

    def color(self, fg: Color, bg: Color):
        """Set the default foreground and background colors."""
        self.fg_color, self.bg_color = fg, bg
        return self

    def write(self, text: Union[Text, CharCode, List[CharCode]],
                 at: Point, fg_color: Color = None, bg_color: Color = None):
        """Write text at the specified position.
        A string or list of charcodes or a charcode can be passed as the
        text parameter.

        If no colors are specified, the default colors are used.
        """
        if isinstance(text, CharCode):
            text = [text]
        if (at not in self.size or
            at[0] + len(text) - 1 >= self.size.top_right.x):
            raise ValueError('writing out of bound')
        fg_color = self.fg_color if fg_color is None else fg_color
        bg_color = self.bg_color if bg_color is None else bg_color
        for pos, char in enumerate(text):
            self.draw_glyph(
                Glyph(char, fg_color, bg_color), Point(at[0] + pos, at[1]))
        return self

    def fill(self, bg: Color, window: Rect):
        """Fill a portion of the terminal with the specified color.
        """
        if window not in self.size:
            raise ValueError('window out of bounds')

        _glyph = Glyph(CharCode.SPACE, None, bg)
        for _y in range(window[1], window[3]):
            for _x in range(window[0], window[2]):
                self.draw_glyph(_glyph, Point(_x, _y))
        return self

    def clear(self, window: Rect = None):
        """Clear the terminal using the default background color.

        Optionally, a `window` argument can be passed to clear just
        that portion.
        """
        window = self.size if window is None else window
        if window not in self.size:
            raise ValueError('window out of bounds')

        self.fill(self.bg_color, window)
        return self

    def view(self, window: Rect):
        """Return a sub view into the terminal, see `Subterminal`.
        """
        return Subterminal(self, window)

    @abstractmethod
    def draw_glyph(self, glyph_: Glyph, at: Point):
        """Draw a glyph at the specified position.

        implementations may or may not render the result of writing
        to the screen.
        """
        pass


class Subterminal(Terminal):
    """Provide a way to treat a portion of the root terminal as a
    standalone terminal. Implements `Terminal` ABC.

    additional properties:
        root -- the root/parent terminal.

    Any writes to the subterminal are writes to the root terminal.
    """

    def __init__(self, root: Terminal, window: Rect):
        if window not in root.size:
            raise ValueError('window out of bounds')
        super().__init__((window[2], window[3]))
        self.view_window = Rect(*window)
        self._root = root

    @property
    def root(self):
        return self._root

    # override to eliminate nested subterminals
    def view(self, window: Rect):
        if window not in self.size:
            raise ValueError('window out of bounds')
        return Subterminal(self._root, window)

    def draw_glyph(self, glyph_: Glyph, at: Point):
        point = Point(self.view_window.x + at[0],
                      self.view_window.y + at[1])
        self._root.draw_glyph(glyph_, point)


class RenderableTerminal(Terminal, ABC):
    """A renderable terminal is a terminal that guarantees the results of
    writes are fully written after the `render` method is called.
    """
    @abstractmethod
    def render(self):
        """Render the terminal displaying all writes to the screen.
        """
        pass
