from typing import NamedTuple

_Color = NamedTuple('Color', [('r', int), ('g', int), ('b', int)])


class Color(_Color):
    def add(self, other: 'Color', fraction_other: float = 1.0):
        return Color(
            int(max(0, min(255, self.r + other.r * fraction_other))),
            int(max(0, min(255, self.g + other.g * fraction_other))),
            int(max(0, min(255, self.b + other.b * fraction_other))))

    def blend(self, other: 'Color', fraction_other: float):
        fraction_this = 1.0 - fraction_other
        return Color(
            int(self.r * fraction_this + other.r * fraction_other),
            int(self.g * fraction_this + other.g * fraction_other),
            int(self.b * fraction_this + other.b * fraction_other))

    def blend_percent(self, other: 'Color', percent_other: int):
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
