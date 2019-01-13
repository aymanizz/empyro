from typing import NamedTuple

Point = NamedTuple('Point', [('x', int), ('y', int)])

Size = NamedTuple('Size', [('width', int), ('height', int)])

_Rect = NamedTuple(
    'Rect', [('x', int), ('y', int), ('width', int), ('height', int)])


class Rect(_Rect):
    @property
    def top_left(self) -> Point:
        return Point(self.x, self.y)

    @property
    def bottom_right(self) -> Point:
        return Point(self.x + self.width, self.y + self.height)

    @property
    def top_right(self) -> Point:
        return Point(self.x + self.width, self.y)

    @property
    def bottom_left(self) -> Point:
        return Point(self.x, self.y + self.height)

    def __contains__(self, other):
        if isinstance(other, Rect):
            return (contains_point(self, other.top_left) and
                    contains_point(self, other.bottom_right))
        elif isinstance(other, Point):
            return contains_point(self, other)
        raise TypeError('object must be of type Rect or Point')

    def _contains_point(self, point: Point) -> bool:
        return (self.x + self.width >= point.x >= self.x and
                self.y + self.height >= point.y >= self.y)
