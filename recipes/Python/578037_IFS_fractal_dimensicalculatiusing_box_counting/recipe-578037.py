# IFS fractal dimension calculation using box-counting method
# http://en.wikipedia.org/wiki/Iterated_function_system
# http://en.wikipedia.org/wiki/Fractal_dimension
# http://en.wikipedia.org/wiki/Box-counting_dimension
# http://en.wikipedia.org/wiki/Simple_linear_regression
# FB - 20120211
import math
import random
from PIL import Image
imgx = 512
imgy = 512 # will be auto-re-adjusted according to aspect ratio of the fractal
maxIt = imgx * imgy * 2

fractalName = "Barnsley Fern"
mat=[[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
     [0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85],
     [0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
     [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]

##fractalName = "Centipede"
##mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
##       [0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]

##fractalName = "Levy C curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]

##fractalName = "Dragon curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]

##fractalName = "Sierpinski Triangle"
##mat = [[0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.33],
##       [0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.33],
##       [0.5, 0.0, 0.0, 0.5, 0.0, 0.5, 0.33]]

##fractalName = "Sierpinski Carpet"
##mat = [[0.333, 0.0, 0.0, 0.333, 0.000, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.333, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.000, 0.666, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.666, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.000, 0.333, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.333, 0.333, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.333, 0.125]]

m = len(mat) # number of IFS transformations
# find xmin, xmax, ymin, ymax of the fractal using IFS algorithm
x = mat[0][4]
y = mat[0][5] 
xa = x
xb = x
ya = y
yb = y
for k in range(maxIt):
    i = random.randint(0, m - 1)
    if random.random() <= mat[i][6]:
        x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
        y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
        x = x0 
        if x < xa:
            xa = x
        if x > xb:
            xb = x
        if y < ya:
            ya = y
        if y > yb:
            yb = y

imgy = int(imgy * (yb - ya) / (xb - xa)) # auto-re-adjust the aspect ratio 
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()

# drawing using IFS algorithm
theColor = (255, 255, 255)
x=0.0
y=0.0 
for k in range(maxIt):
    i = random.randint(0, m - 1)
    if random.random() <= mat[i][6]:
        x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
        y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
        x = x0 
        jx = int((x - xa) / (xb - xa) * (imgx - 1)) 
        jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
        if jx >= 0 and jx < imgx and jy >= 0 and jy < imgy:
            pixels[jx, jy] = theColor
image.save(fractalName + " fractal.png", "PNG")

# fractal dimension calculation using box-counting method
b = 2 # initial box size in pixels
f = 2 # box scaling factor
n = 3 # number of graph points for simple linear regression
gx = [] # x coordinates of graph points
gy = [] # y coordinates of graph points
for ib in range(n):
    bs = b * f ** ib # box size in pixels
    bnx = int(imgx / bs) # of boxes in x direction of image
    bny = int(imgy / bs) # of boxes in y direction of image
    boxCount = 0
    for by in range(bny):
        for bx in range(bnx):
            # if there are any pixels in the box then increase box count
            foundPixel = False
            for ky in range(bs):
                for kx in range(bs):
                    if pixels[bs * bx + kx, bs * by + ky] == theColor:
                        foundPixel = True
                        boxCount += 1
                        break
                if foundPixel:
                    break
    gx.append(math.log(1.0 / bs))
    gy.append(math.log(boxCount))
    
# simple linear regression
x_ = 0.0
y_ = 0.0
x2_ = 0.0
xy_ = 0.0
for j in range(n):
    x_ += gx[j]
    y_ += gy[j]
    x2_ += gx[j] ** 2
    xy_ += gx[j] * gy[j]
x_ = x_ / n
y_ = y_ / n
x2_ = x2_ / n
xy_ = xy_ / n
b = (xy_ - x_ * y_) / (x2_ - x_ ** 2) # slope of the regression line
# a = y_ - b * x_

print "Fractal Name: " + fractalName
print "Estimated Fractal Dimension: " + str(b)
