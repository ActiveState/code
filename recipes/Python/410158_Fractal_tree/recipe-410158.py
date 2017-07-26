#/usr/bin/env python

import Tkinter, sys
from math import sqrt, pi, atan2
from cmath import exp
from optparse import OptionParser

def get_parent_indices(i, j, nbran):
    return (i-1, j//nbran)

class fractal_tree:

    def __init__(self, ratio=0.8, angle=pi/2., ngen=3, nbran=2):
        """
        ratio: ratio of branch length with respect to previous generation
        angle: fan angle, how wide spread the branches will be (0<angle<2*pi)
        ngen: number of generations.
        nbran: number of new branches.
        """
        # coords in complex notation
        self.ratio = ratio
        self.angle = angle
        self.ngen  = ngen
        self.nbran = nbran
        # the root is at (0,0)
        # the top of the trunk is at position (0,1), this will be the
        # starting node
        self.pts2xy = {(-1,0): 0j, (0,0): 1j}
        self.xmax, self.ymax = 0, 1
        alpha_0     = angle/2.
        delta_alpha = angle / float(nbran-1)
        for i in range(1, ngen):
            for j in range(nbran**i):
                # child
                ij = (i,j)
                # parent
                kl = get_parent_indices(i, j, nbran)
                k, l = kl
                xy_kl = self.pts2xy[kl]
                xy_mn = self.pts2xy[(k-1, l//nbran)] 
                ph_ij = atan2(xy_kl.imag - xy_mn.imag, xy_kl.real - xy_mn.real)
                self.pts2xy[ij] = self.pts2xy[kl] + \
                                  ratio**i * \
                                  exp(1j*(ph_ij+ alpha_0 - (j%nbran)*delta_alpha))
                x, y = self.pts2xy[ij].real, self.pts2xy[ij].imag
                self.xmax = max(x, self.xmax)
                self.ymax = max(y, self.ymax)

    def get_pixel_coordinates(self, x, y, width, height):
        xpix = 0.5 * width * (1 + x/self.xmax)
        ypix = height * (1. - y/self.ymax)
        return (xpix, ypix)
        
    def draw(self, root, height=600):
        """
        Draw the tree using Tkinter
        """
        aspect_ratio = 2*self.xmax/self.ymax
        width = aspect_ratio*height
        canvas = Tkinter.Canvas(root, height=height, width=width,
                                background='white')
        canvas.pack()
        for i in range(0, self.ngen):
            for j in range(max(1, self.nbran**i)):
                ij = (i,j)
                x, y = self.pts2xy[ij].real, self.pts2xy[ij].imag
                xpix, ypix = self.get_pixel_coordinates(x,y,
                                                        width=width,
                                                        height=height)
                # parent
                kl = get_parent_indices(i,j, self.nbran)
                u, v = self.pts2xy[kl].real, self.pts2xy[kl].imag
                upix, vpix = self.get_pixel_coordinates(u, v,
                                                   width=width,
                                                   height=height)
                canvas.create_line(upix,vpix, xpix,ypix, fill='black')
        
                
            
            

##############################################################################
def main():
    parser = OptionParser()
    parser.add_option('-r', '--ratio', action='store', type="float",
                  dest="ratio",
                  help='Ratio of branch length with respect to previous generation (<1.).',
                  default=0.5,
                  )
    parser.add_option('-n', '--ngen', action='store', type="int",
                  dest="ngen",
                  help='Number of generations (>1).',
                  default=4,
                  )
    parser.add_option('-y', '--ysize', action='store', type="int",
                  dest="ysize",
                  help='Number of vertical pixels.',
                  default=400,
                  )
    parser.add_option('-a', '--angle', action='store', type="float",
                  dest="angle",
                  help='Fan angle between group of branches in deg.',
                  default=90,
                  )
    parser.add_option('-N', '--Nbran', action='store', type="int",
                  dest="nbran",
                  help='Number of new branches.',
                  default=2,
                  )
    options, args = parser.parse_args(sys.argv)
    t = fractal_tree(ngen=options.ngen, ratio=options.ratio,
                     angle=options.angle*pi/180.0, nbran=options.nbran)
    root = Tkinter.Tk()
    t.draw(root, height=options.ysize)
    root.mainloop()
if __name__=='__main__': main()
