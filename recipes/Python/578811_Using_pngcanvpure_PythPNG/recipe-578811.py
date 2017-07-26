#!/usr/bin/env python

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import io
import logging

from pngcanvas import *

BUFSIZE = 8*1024  # Taken from filecmp module
HEIGHT = WIDTH = 512

logging.debug("Creating canvas: %d, %d", WIDTH, HEIGHT)
c = PNGCanvas(WIDTH, HEIGHT, color=(0xff, 0, 0, 0xff))
c.rectangle(0, 0, WIDTH - 1, HEIGHT - 1)

logging.debug("Generating gradient...")
c.vertical_gradient(1, 1, WIDTH - 2, HEIGHT - 2,
    (0xff, 0, 0, 0xff), (0x20, 0, 0xff, 0x80))

logging.debug("Drawing some lines...")
c.color = bytearray((0, 0, 0, 0xff))
c.line(0, 0, WIDTH - 1, HEIGHT - 1)
c.line(0, 0, WIDTH / 2, HEIGHT - 1)
c.line(0, 0, WIDTH - 1, HEIGHT / 2)

with open("try_pngcanvas.png", "wb") as png_fil:
    logging.debug("Writing to file...")
    png_fil.write(c.dump())
