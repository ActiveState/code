# Recursively draw the Mandelbrot set
# Dependencies: Python 2.7.5, PyGame 1.9.1

import pygame
from pygame.locals import QUIT
from sys import exit

# size must be a power of 2 or you will get rounding errors in the image
# E.g. 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, ...
size = 512

pygame.init()
surface = pygame.display.set_mode((size, size), 0, 32)

# Mandelbrot drawing area
xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5

# maximum iterations
maxIt = 256

def pump():
    # pump the event queue so the window is responsive, exit if signaled
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

def point(x, y):
    # get the escape value of a specific coordinate in the Mandelbrot set
    zy = y * (yb - ya) / size  + ya
    zx = x * (xb - xa) / size  + xa
    z = zx + zy * 1j
    c = z
    for i in xrange(maxIt):
        if abs(z) > 2.0: break
        z = z * z + c
    return i

def col(c):
    # return a color variable computed from a escape value
    return (c % 4 * 64, c % 8 * 32, c % 16 * 16)

def mandel(x, y, i_size):
    p1 = point(x, y)
    half = i_size / 2
    # if half > 1 then there are still possible sub-divisions
    if half > 1:
        # if all the pixels around the square are the same then it can just
        # be filled instead of sub-divided - test the square
        test = False
        for i in xrange(i_size):
            t1 = point(x, y + i)
            t2 = point(x + i, y)
            t3 = point(x + i_size, y + i)
            t4 = point(x + i, y + i_size)
            if (p1 != t1 or p1 != t2 or p1 !=t3 or p1 != t4):
                test = True
                break
        if test:
            # The colors all around the square are not equal so sub-divide
            mandel(x, y, half)
            mandel(x + half, y, half)
            mandel(x + half, y + half, half)
            mandel(x, y + half, half)
        else:
            # This is a base case, all square border points are same color
            # fill area and return back up the stack
            surface.fill(col(p1), (x, y, i_size, i_size))
    else:
        # This is a base case, a 2x2 block. Plot the four pixels
        # and return back up the stack
        p2 = point(x + i_size - 1, y)
        p3 = point(x + i_size - 1, y + i_size - 1)
        p4 = point(x, y + i_size - 1)
        surface.lock()
        surface.set_at((x, y), col(p1))
        surface.set_at((x + i_size - 1, y), col(p2))
        surface.set_at((x + i_size - 1, y + i_size - 1), col(p3))
        surface.set_at((x, y + i_size - 1), col(p4))
        surface.unlock()

    pygame.display.update()
    pump()

# calculate the image
mandel(0, 0, size)

# Wait for user to click close widget on window
while True:
    pump()
