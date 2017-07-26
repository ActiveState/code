from collections import namedtuple

Point = namedtuple('Point', 'x, y')

POINTS = (
    Point(610, 102),
    Point(253, 241),
    Point(341, 446),
    Point(357, 42),
    Point(153 ,336),
    Point(203, 125),
    Point(306, 492),
    Point(335, 57),
    Point(38, 400),
    Point(191, 357),
    # and many, many more points.
)
print POINTS

##
## Ok, we decided 3D is way cooler.
## But only a few points have a z coordinate != 0.
## 
Point = namedtuple('Point', 'x, y z')

##
## The solution is quite simple.
## Our on-the-fly partial adapter!
##
from functools import partial

Point = partial(Point, z = 0)

POINTS = (
    Point(610, 102),
    Point(253, 241),
    Point(341, 446, z = 23),
    # But, however, our defaults have to be specified as keyword arguments.
    # Otherwise we got a complaint:
    #   TypeError: __new__() got multiple values for keyword argument 'z'
    Point(357, 42),
    Point(153 ,336, z = 11),
    Point(203, 125),
    Point(306, 492, z = 42),
    Point(335, 57),
    Point(38, 400, z = 47),
    Point(191, 357),
)
print POINTS
