"""Module for coordinates classes.

Classes defined:
    Point -- represent a point in 2D space, a tuple of 2 values: x and y.
    Size  -- represent the size of an object in 2D space,
             a tuple of 2 values: width and height.
    Rect  -- represent a rectangle in 2D space,
             a tuple of 4 values: x, y, width, and height.
"""

from typing import NamedTuple, Union

Point = NamedTuple('Point', [('x', int), ('y', int)])

Size = NamedTuple('Size', [('width', int), ('height', int)])

_Rect = NamedTuple(
    'Rect', [('x', int), ('y', int), ('width', int), ('height', int)])


class Rect(_Rect):
    """Represent a rectangle.
    A tuple of 4 values: x, y, width, height.

    Defines the following properties for getting the rectangle corners:
        top_left, top_right, bottom_right
    """

    @property
    def size(self) -> Size:
        """The size of the rectangle.

        >>> Rect(1, 2, 3, 4).size == Size(3, 4)
        True
        """
        return Size(self.width, self.height)

    @property
    def center(self) -> Point:
        """The center of the rectangle.

        >>> Rect(0, 0, 4, 6).center == Point(2, 3)
        True
        """
        return Point(self.width // 2, self.height // 2)

    @property
    def top_left(self) -> Point:
        """The top left corner point of the rectangle

        >>> Rect(1, 2, 3, 4).top_left == Point(1, 2)
        True
        """
        return Point(self.x, self.y)

    @property
    def bottom_right(self) -> Point:
        """The bottom right corner point of the rectangle

        >>> Rect(1, 2, 3, 4).bottom_right == Point(4, 6)
        True
        """
        return Point(self.x + self.width, self.y + self.height)

    @property
    def top_right(self) -> Point:
        """The top right corner point of the rectangle

        >>> Rect(1, 2, 3, 4).top_right == Point(4, 2)
        True
        """
        return Point(self.x + self.width, self.y)

    @property
    def bottom_left(self) -> Point:
        """The bottom left corner point of the rectangle

        >>> Rect(1, 2, 3, 4).bottom_left == Point(1, 6)
        True
        """
        return Point(self.x, self.y + self.height)

    def __contains__(self, other: Union['Rect', Point]) -> bool:
        """Whether a rectangle or a point is located inside the self rectangle.

        >>> (1, 2) in Rect(4, 4, 8, 8)
        False
        >>> (5, 6) in Rect(4, 4, 8, 8)
        True
        >>> (4, 4, 8, 8) in Rect(4, 4, 8, 8)
        True
        >>> (2, 2, 2, 2) in Rect(2, 1, 5, 3)
        True
        >>> (1, 2, 3, 4) in Rect(4, 4, 4, 4)
        False
        >>> (5, 5, 10, 10) in Rect(5, 5, 10, 10)
        True
        >>> (15, 15) in Rect(5, 5, 10, 10)
        False
        """
        _len = len(other)
        if _len == 2:
            return self._contains_point(other)
        elif _len == 4:
            return (self._contains_point((other[0], other[1])) and
                    self.x + self.width >= other[0] + other[2] and
                    self.y + self.height >= other[1] + other[3])
        raise TypeError('left operand must be of type Rect, '
                        'Point, or a sequence of length 2 or 4')

    def _contains_point(self, point: Point) -> bool:
        return (self.x <= point[0] < self.x + self.width and
                self.y <= point[1] < self.y + self.height)
