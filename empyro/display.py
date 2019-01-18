"""Provide a way to manage the display state in an efficient way.

This is achieved by maintaining a dict of the cells changed from last update.
This way a change only has a cost if it's really a change,
i.e. the glyph have actually changed between the last update and the current
update.

Multiple writes that result in the same glyph that was in the cell from last
update will have no effect, and will not be on the changed glyphs dict.
"""

from typing import Callable, KeysView

from . import glyph
from .glyph import Glyph
from .coord import Point, Size, Rect


class Display:
    def __init__(self, size: Size,
                 render_callback: Callable[[Glyph, Point], None] = None):
        self.size = Rect(0, 0, *size)
        self._cells = [
            [glyph.CLEAR for y in range(self.size.height)]
            for x in range(self.size.width)
        ]
        self._changed_cells = {}
        self.render_callback = render_callback

    def get_dirty_cells(self) -> KeysView:
        """Get the positions of the changed glyphs.
        """
        return self._changed_cells.keys()

    def set_glyph(self, glyph_: Glyph = None, at: Point):
        """Set the cell at `at` to `glyph_`
        """
        if at not in self.size:
            raise ValueError('out of bounds error')
        if self._cells[at[0]][at[1]] == glyph_:
            self._changed_cells.pop(at, None)
        else:
            self._changed_cells[at] = glyph_

    def render(self):
        """Call the `render_callback` for the changed cells.
        """
        for (x, y), glyph in self._changed_cells.items():
            self.render_callback(glyph, (x, y))
            self._cells[x][y] = glyph
        self._changed_cells.clear()
