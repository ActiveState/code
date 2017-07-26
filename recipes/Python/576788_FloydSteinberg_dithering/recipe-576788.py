#!/usr/bin/env python

""" Floyd-Steinberg Dithering algorithm, see:
    http://en.wikipedia.org/wiki/Floyd-Steinberg
"""

import sys
import os

from math import sqrt
from Numeric import *

fs_coeffs = [7.0,3.0,5.0,1.0]

class Dither:

    def __init__(self,pixels,xl,yl):

        self.pixels = pixels
        self.xl = xl
        self.yl = yl

        self.fs_dither()

    def _find_closest_palette_color(self, oldpixel): 
        return int(oldpixel + 0.5)

    def fs_dither(self):

        A,B,G,S = map(lambda x : float(x)/16.0, fs_coeffs)

        for y in xrange(self.yl):
            for x in xrange(self.xl):
                oldpixel = self.pixels[x][y]
                newpixel = self._find_closest_palette_color(oldpixel)
                self.pixels[x][y] = float(newpixel)
                quant_error = float(oldpixel - newpixel)
                if (x < self.xl - 1):
                    self.pixels[x+1][y] += (A * quant_error)
                if (x > 0) and (y < self.yl - 1):
                    self.pixels[x-1][y+1] += (B * quant_error)
                if (y < self.yl - 1):
                    self.pixels[x][y+1] += (G * quant_error)
                if (x < self.xl - 1) and (y < self.yl - 1):
                    self.pixels[x+1][y+1] += (S * quant_error)


if __name__=='__main__':

    """ Form an xl-by-yl array """
    xl = yl = 20
    initpixels = reshape((0.5,) * xl * yl ,[xl,yl])

    """ Dither """
    D = Dither(initpixels,xl,yl)
    print D.pixels

    """ Import the R stats package libraries
        and create a matrix of the dither pixels
    """
    import rpy as R
    z_lst = []
    [z_lst.extend(i) for i in D.pixels]
    z = R.r.matrix(z_lst, byrow=R.r.FALSE, ncol=xl)
            
    """ Create a plot of the dithered image """
    R.r.pdf("dither_plot.pdf")
    R.r.image(range(xl),range(yl),z)
    R.r.dev_off()
