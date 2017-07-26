# Date : 29th July
# Author : Alexander Baker

import sys
from pylab import figure, show, clf, savefig, cm
from numpy.fft import fft, fft2, ifft, ifft2, fftshift
from optparse import OptionParser
from numpy import *


def generateResolution(n):
   return 2**n, (2**n)-1

def store_value(option, opt_str, value, parser):
    setattr(parser.values, option.dest, value)
   
def main():

   parser = OptionParser()

   parser.add_option("-r", "--resolution", action="callback", callback=store_value, type="int", nargs=1, dest="resolution", help="resolution of the grid parameter")   
   parser.add_option("-g", "--grid", action="callback", callback=store_value, type="int", nargs=1, dest="grid", help="grid size parameter")   
   parser.add_option("-s", "--steps", action="callback", callback=store_value, type="int", nargs=1, dest="steps", help="number of steps")
   parser.add_option("-b", "--beam", action="callback", callback=store_value, type="int", nargs=1, dest="beam", help="beam size")
   parser.add_option("-c", "--core", action="callback", callback=store_value, type="float", nargs=1, dest="core", help="beam size")
   parser.add_option("-p", "--phase", action="callback", callback=store_value, type="int", nargs=1, dest="phase", help="phase size parameter")   
   parser.add_option("-i", "--image", action="callback", callback=store_value, type="string", nargs=1, dest="image", help="phase size parameter")   

   (options, args) = parser.parse_args()
   
   grid_resolution = 6       
   grid_size = 8
   steps = 35
   beam = 8
   core = 0.3
   phase = 15
   image = 'bw'
   
   if options.resolution:
      grid_resolution = options.resolution   
      
   if options.grid:
      grid_size = options.grid       

   if options.steps:
      steps = options.steps

   if options.beam:
      beam = options.beam

   if options.core:
      core = options.core
      
   if options.phase:
      phase = options.phase

   if options.image:
      image = options.image

   print '\n######################################################'
   print '# Numerical Lattice Model'
   print '# Alexander Baker - August 2007'
   print '######################################################\n'

   grid_resolution, grid_resolution_1 = generateResolution(grid_resolution)
   
   # The grid size effects the number of steps we apply to get to the upper limit

   print "grid_size : [%d]\ngrid_resolution [%d]\ngrid_resolution-1 [%d]" %(grid_size, grid_resolution, grid_resolution_1)

   x1 = arange(-1 * 1.0* grid_size,(-1 * grid_size) + grid_resolution_1 * 1.0 * (2 * grid_size)/grid_resolution, (grid_size * 1.0)/grid_resolution)

   x2 = arange(-1 * 1.0 * grid_size,(-1 * grid_size) + grid_resolution_1 * 1.0 * (2 * grid_size)/grid_resolution, (grid_size * 1.0)/grid_resolution)

   xmin, xmax, ymin, ymax = -1 * 1.0 * grid_size, (-1 * grid_size) + grid_resolution_1 * 1.0 * (2 * grid_size)/grid_resolution, -1 * 1.0 * grid_size, (-1 * grid_size) + grid_resolution_1 * 1.0 * (2 * grid_size)/grid_resolution
   extent = xmin, xmax, ymin, ymax

   print "\ngrid extent X-[%f][%f] Y-[%f][%f]" % (xmin, xmax, ymin, ymax)
   print "shape x1", shape(x1)
   print "shape x2", shape(x2)
   print "step [%f]" % ((grid_size * 1.0)/grid_resolution)
   print "start [%f], end[%f]" % (-1 * 1.0* grid_size, grid_resolution_1 * 1.0 * (2 * grid_size)/grid_resolution)

   [x1,x2] = meshgrid(x1,x2)

   rbeam = beam
   wcore = core
   vpos = 1
   _del = 1


   print "\nrbeam [%d]\nwcore [%f]\nvpos [%f]\n_del [%f]" % (rbeam, wcore, vpos, _del)

   #
   # Step 1. Take your initial beam profile (gaussian, a vortex etc etc) at z = 0
   #
   
   y = 1.0*exp(-2*(x1**2 + x2**2)/rbeam**2)*exp(1j* phase *(+arctan2(x2,x1))) * tanh(pow((x1**2 + x2**2), 0.5)/wcore)           

   fig1 = figure(1)
   fig1.clf()
   ax1a = fig1.add_subplot(121)

   if image == 'bw':
	   ax1a.imshow(angle((y)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
   else:
	   ax1a.imshow(angle((y)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
   ax1a.set_title(r'Angle')
   ax1b = fig1.add_subplot(122)

   if image == 'bw':
       ax1b.imshow(abs((y)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
   else:
       ax1b.imshow(abs((y)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)

   ax1b.set_title(r'Amplitude')
   savefig('big_start_' + str(wcore)+'_' + str(vpos) +'.png')  

   u1 = arange(-1.0,-1+1.0*grid_resolution_1* ((2 * 1.0)/grid_resolution), 1.0/grid_resolution)
   u2 = arange(-1.0,-1+1.0*grid_resolution_1* ((2 * 1.0)/grid_resolution), 1.0/grid_resolution)

   u1min, u1max, u2min, u2max = -1.0, -1+1.0*grid_resolution_1* ((2 * 1.0)/grid_resolution), -1.0, -1+1.0*grid_resolution_1* ((2 * 1.0)/grid_resolution)

   print "\npropagation grid X-[%f][%f] Y-[%f][%f]" % (u1min, u1max, u2min, u2max)

   print "shape u1", shape(u1)
   print "shape u2", shape(u2)
   
   print "step [%f]" % (1.0/grid_resolution)
   print "start [%f], end[%f]" % (-1.0, -1+1.0*grid_resolution_1* ((2 * 1.0)/grid_resolution))

   print "\nbeam power (start) - [%f]" % (sum(sum(abs(y**2))))

   [u1,u2] = meshgrid(u1,u2)

   t = exp(2*pi*1j*(u1**2 + u2**2)*_del)
   w = fftshift(t)

   #
   # Step 2. Split step progagation
   #

   for i in arange(100,100+steps, 1):
     z = fft2(y)
     zp = z * w   
     yp = ifft2(zp)
     p = (exp(+0.01*pi*1j*(x1**2 + x2**2)*_del + 0.05*pi*1j*y*conj(y))*_del); 
     yp = yp * p
     y = yp
     zp = fft2(yp)
     zp = zp * w
     yp = ifft2(zp)

     fig3 = figure(3)
     fig3.clf()
     ax3 = fig3.add_subplot(111)

     if image == 'bw':   
        ax3.imshow(abs((yp)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
     else:
        ax3.imshow(abs((yp)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)

     ax3 = fig3.add_subplot(111)
     if image == 'bw':   
        ax3.imshow(angle((yp)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
     else :
        ax3.imshow(angle((yp)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)    

     print sum(sum(abs(yp**2))), i-100
   print "beam power (end) - [%f]" % (sum(sum(abs(yp**2))))

   fig2 = figure(2)
   fig2.clf()
   ax2a = fig2.add_subplot(121)
   if image == 'bw':   
      ax2a.imshow(angle((yp)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
   else:
      ax2a.imshow(angle((yp)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
   ax2a.set_title(r'Angle')
   ax2b = fig2.add_subplot(122)
   if image == 'bw':   
      ax2b.imshow(abs((yp)), cmap=cm.gist_gray, alpha=.9, interpolation='bilinear', extent=extent)
   else:
      ax2b.imshow(abs((yp)), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
   ax2b.set_title(r'Amplitude')
   savefig('big_end_' + str(wcore)+'_' + str(vpos) +'.png')  

   print '\ndone. ok'

if __name__ == "__main__":   
   main()      
