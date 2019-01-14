"""Provide color class and manipulation methods.

defines the following:
    Color -- class for representing a color in rgb format.
    Some color constants, provided for convenience.
"""

from typing import NamedTuple

_Color = NamedTuple('Color', [('r', int), ('g', int), ('b', int)])


class Color(_Color):
    """Represent an rgb color value."""
    def add(self, other: 'Color', fraction_other: float = 1.0):
        """Add one color to another and return it.

        >>> Color(15, 15, 15).add(Color(15, 15, 15)) == Color(30, 30, 30)
        True
        >>> Color(245, 245, 15).add(Color(15, 15, 15)) == Color(255, 255, 30)
        True
        >>> Color(10, 10, 10).add(Color(10, 10, 10), 0.5) == Color(15, 15, 15)
        True
        """
        return Color(
            int(max(0, min(255, self.r + other.r * fraction_other))),
            int(max(0, min(255, self.g + other.g * fraction_other))),
            int(max(0, min(255, self.b + other.b * fraction_other))))

    def blend(self, other: 'Color', fraction_other: float):
        """Blend one color with another using fraction_other to
        determine the percentages.

        >>> Color(10, 10, 10).blend(Color(100, 100, 100), 0.1) == \
            Color(19, 19, 19)
        True
        """
        fraction_this = 1.0 - fraction_other
        return Color(
            int(self.r * fraction_this + other.r * fraction_other),
            int(self.g * fraction_this + other.g * fraction_other),
            int(self.b * fraction_this + other.b * fraction_other))

    def blend_percent(self, other: 'Color', percent_other: int):
        """Blend one color with another using percent_other to
        determine the percentages.

        >>> Color(10, 10, 10).blend_percent(Color(100, 100, 100), 10) == \
            Color(19, 19, 19)
        True
        """
        return self.blend(other, percent_other / 100)

    def __hash__(self):
        return self.r ^ self.g ^ self.b


BLACK = Color(0, 0, 0)
RED = Color(128, 0, 0)
GREEN = Color(0, 128, 0)
YELLOW = Color(128, 128, 0)
BLUE = Color(0, 0, 128)
MAGENTA = Color(128, 0, 128)
CYAN = Color(0, 128, 128)
WHITE = Color(192, 192, 192)
BRIGHT_BLACK = Color(128, 128, 128)
BRIGHT_RED = Color(255, 0, 0)
BRIGHT_GREEN = Color(0, 255, 0)
BRIGHT_YELLOW = Color(255, 255, 0)
BRIGHT_BLUE = Color(0, 0, 255)
BRIGHT_MAGENTA = Color(255, 0, 255)
BRIGHT_CYAN = Color(0, 255, 255)
BRIGHT_WHITE = Color(255, 255, 255)
