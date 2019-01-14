from typing import NamedTuple, Union

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

    def __contains__(self, other: Union['Rect', Point]):
        _len = len(other)
        if _len == 2:
            return self._contains_point(other)
        elif _len == 4:
            other = Rect(*other)
            return (self._contains_point(other.top_right) and
                    self._contains_point(other.bottom_left))
        raise TypeError('left operand must be of type Rect, '
                        'Point, or a sequence of length 2 or 4')

    def _contains_point(self, point: Point) -> bool:
        return (self.x + self.width >= point.x >= self.x and
                self.y + self.height >= point.y >= self.y)
