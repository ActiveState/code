#!/usr/bin/env python

import cairo

w, h = 128, 128

# Setup Cairo
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
ctx = cairo.Context(surface)

# Set thickness of brush
ctx.set_line_width(15)

# Draw out the triangle using absolute coordinates
ctx.move_to(w/2, h/3)
ctx.line_to(2*w/3, 2*h/3)
ctx.rel_line_to(-1*w/3, 0)
ctx.close_path()

# Apply the ink
ctx.stroke()

# Output a PNG file
surface.write_to_png("triangle.png")

# Alias the image as a numpy array
import numpy

# This needs better than pycairo-1.2.2, eg. pycairo CVS:
# cvs -d :pserver:anoncvs@cvs.freedesktop.org:/cvs/cairo co pycairo
buf = surface.get_data()

a = numpy.frombuffer(buf, numpy.uint8)
a.shape = (w, h, 4)

a[:,:,2] = 255
surface.write_to_png("triangle1.png") # red triangle..

# Alias the image as a pygame surface
import pygame
from time import sleep

imsurf = pygame.image.frombuffer(buf, (w,h), "RGBA")
depth = 4*8

pygame.display.init()
surface = pygame.display.set_mode((w,h), pygame.DOUBLEBUF, depth)

done = False
while not done:
    surface.blit(imsurf, (0,0)) # blue triangle..
    sleep(0.1)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
