'''Module for physics simulation.

This module provides two classes that allow the
approximation of physics behind bouncing balls.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 20, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
B. Brown, for teaching me some math courses.
C. Parker, for freely providing boids pseudocode.'''

################################################################################

import math as _math
import sys as _sys

################################################################################

class Vector:

    'Vector(x, y) -> Vector'

    def __init__(self, x, y):
        'Initialize the Vector object.'
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        'Return the vector\'s representation.'
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __iter__(self):
        'Return an iterator.'
        yield self.x
        yield self.y

    def __add__(self, vector):
        'Return the sum of vector addition.'
        return Vector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        'Return the difference of vector subtraction.'
        return Vector(self.x - vector.x, self.y - vector.y)

    def __mul__(self, number):
        'Return the product of vector multiplication.'
        return Vector(self.x * number, self.y * number)

    def __div__(self, number):
        'Return the quotient of vector division.'
        return Vector(self.x / number, self.y / number)

    def __iadd__(self, vector):
        'Execute addition in-place.'
        self.x += vector.x
        self.y += vector.y
        return self

    def __isub__(self, vector):
        'Execute subtraction in-place.'
        self.x -= vector.x
        self.y -= vector.y
        return self

    def __imul__(self, number):
        'Execute multiplication in-place.'
        self.x *= number
        self.y *= number
        return self

    def __idiv__(self, number):
        'Execute division in-place.'
        self.x /= number
        self.y /= number
        return self

    def __abs__(self):
        'Return the vector\'s magnitude.'
        return _math.hypot(self.x, self.y)

    def unit(self):
        'Return the unit vector.'
        return self / abs(self)

################################################################################

class Ball:

    'Ball(x, y, radius) -> Ball'

    def __init__(self, x, y, radius):
        'Initialize the Ball object.'
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.err = Vector(0, 0)
        self.rad = radius

    def crash(self, ball):
        'Try to crash two balls together.'
        p = ball.pos - self.pos
        a = abs(p)
        if a <= self.rad + ball.rad:
            v = self.vel - ball.vel
            s = _sub(_ang(p), _ang(v))
            if s < _PI_D_2:
                e =  p * (_math.cos(s) * abs(v) / a)
                ball.err += e
                self.err -= e

    def correct(self):
        'Update the ball\'s velocity.'
        self.vel += self.err
        self.err = Vector(0, 0)

    def move(self, frames_per_second):
        'Update the ball\'s position.'
        self.pos += self.vel / frames_per_second

################################################################################

_PI_M_2 = _math.pi * 2
_PI_D_2 = _math.pi / 2

################################################################################

def _ang(vector):
    'Private module function.'
    return _math.atan2(vector.x, vector.y) % _PI_M_2

def _sub(angle_a, angle_b):
    'Private module function.'
    diff = abs(angle_a - angle_b)
    return _PI_M_2 - diff if diff > _math.pi else diff

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
