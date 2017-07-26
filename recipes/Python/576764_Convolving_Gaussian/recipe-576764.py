def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    size = int(size)    
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)               
    #print size, sizey    
    x, y = mgrid[-size:size+1, -sizey:sizey+1]
    g = exp(-(x**2/float(size)+y**2/float(sizey)))
    return g / g.sum()

def blur_image(im, n, ny=None) :
    """ blurs the image by convolving with a gaussian kernel of typical
        size n. The optional keyword argument ny allows for a different
        size in the y direction.
    """
    g = gauss_kern(n, sizey=ny)
    improc = signal.convolve(im,g, mode='valid')
    return(improc)    

from pylab import figure, show, clf, savefig, cm    
from scipy import *

xmin, xmax, ymin, ymax = -70, 70, -70, 70
extent = xmin, xmax, ymin, ymax

X, Y = mgrid[-70:70, -70:70]
Z = cos((X**2+Y**2)/200.)+ random.normal(size=X.shape)    
#Z = cos((X**2+Y**2)/200.)

fig1 = figure(1)
fig1.clf()
ax1a = fig1.add_subplot(131)
ax1a.imshow(abs(Z), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
ax1a.set_title(r'Noisey')

P = gauss_kern(3)

ax1b = fig1.add_subplot(132)
ax1b.imshow(abs(P), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
ax1b.set_title(r'Convolving Gaussian')

U = blur_image(Z, 3)

ax1c = fig1.add_subplot(133)
ax1c.imshow(abs(U), cmap=cm.jet, alpha=.9, interpolation='bilinear', extent=extent)
ax1c.set_title(r'Cleaned')
savefig('convolve-gaussian.png')
