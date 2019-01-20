"""Provide a way to register changes made through calls to draw
allowing rendering in an efficient way.

This is achieved by maintaining a dict of the cells changed from last update.
This way a change only has a cost if it's really a change,
i.e. the cell have actually changed between the last update and the current
update.

Multiple writes that result in the same glyph that was in the cell from last
update will have no effect, and will not be on the changed glyphs dict.

This module defines:
    DrawMixin -- a mix-in class for RenderableTerminal subclasses.
"""

from typing import Iterator, Tuple

from . import glyph
from .glyph import Glyph
from .coord import Point, Size, Rect


class DrawMixin:
    """A mix-in class for efficient drawing.

    Use this class as a mix-in when implementing the base class
    `RenderableTerminal`, by inheriting from it:
    `class TermImpl(DrawMixin, RenderableTerminal)`.

    The mix-in provides an implementation for the `draw_glyph` abstract method,
    and a generator `consume_changed_cells` for getting the changed cells to
    help implementing `render` abstract method.
    """

    def __init__(self, size: Size = None):
        super().__init__(size)
        self._cells = [
            [glyph.CLEAR for y in range(self.size.height)]
            for x in range(self.size.width)
        ]
        self._changed_cells = {}

    def consume_changed_cells(self) -> Iterator[Tuple[Point, Glyph]]:
        """Generator to consume the modified cells.
        Use it to get the changed cells in the `render` method.

        Yield a tuple of the changed cell position and the new glyph.
        """
        for at, glyph_ in self._changed_cells.items():
            yield at, glyph_
            self._cells[at[0]][at[1]] = glyph_
        self._changed_cells.clear()

    def draw_glyph(self, glyph_: Glyph, at: Point):
        if at not in self.size:
            raise ValueError('draw out of bounds')
        if self._cells[at[0]][at[1]] == glyph_:
            self._changed_cells.pop(at, None)
        else:
            self._changed_cells[at] = glyph_
