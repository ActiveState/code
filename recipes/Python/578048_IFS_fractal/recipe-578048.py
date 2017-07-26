# IFS fractal dimension calculation
# http://en.wikipedia.org/wiki/Iterated_function_system
# http://en.wikipedia.org/wiki/Fractal_dimension
# http://en.wikipedia.org/wiki/List_of_fractals_by_Hausdorff_dimension
# FB - 20120218
import math
import random
from PIL import Image
imgx = 512
imgy = 512 # will be auto-re-adjusted according to aspect ratio of the fractal
maxIt = imgx * imgy * 2

# Circumference of Polygon
# corners must be ordered in clockwise or counter-clockwise direction
def PolygonCircumference(corners):
    n = len(corners) # of corners
    circumference = 0.0
    for i in range(n):
        j = (i + 1) % n
        dx = corners[j][0] - corners[i][0]
        dy = corners[j][1] - corners[i][1]
        circumference += math.hypot(dx, dy)
    return circumference

##fractalName = "Barnsley Fern"
##mat=[[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 0.01],
##     [0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 0.85],
##     [0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 0.07],
##     [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 0.07]]

##fractalName = "Centipede"
##mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607, 0.787473],
##       [0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795, 0.212527]]

##fractalName = "Levy C curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5]]

##fractalName = "Dragon curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0, 0.5],
##       [-0.5, -0.5, 0.5, -0.5, 1.0, 0.0, 0.5]]

fractalName = "Sierpinski Triangle"
mat = [[0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.33],
       [0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.33],
       [0.5, 0.0, 0.0, 0.5, 0.0, 0.5, 0.33]]

##fractalName = "Sierpinski Carpet"
##mat = [[0.333, 0.0, 0.0, 0.333, 0.000, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.333, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.999, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.000, 0.666, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.666, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.000, 0.333, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.333, 0.333, 0.125],
##       [0.333, 0.0, 0.0, 0.333, 0.666, 0.333, 0.125]]

def IFS(x, y, i): # apply ith transformation to given point
    x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
    y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
    x = x0
    return (x, y)
    
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
        (x, y) = IFS(x, y, i)
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
        (x, y) = IFS(x, y, i)
        jx = int((x - xa) / (xb - xa) * (imgx - 1)) 
        jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
        if jx >= 0 and jx < imgx and jy >= 0 and jy < imgy:
            pixels[jx, jy] = theColor
image.save(fractalName + " fractal.png", "PNG")

# IFS fractal dimension calculation
# calculate scaling coefficients of all transformations
# scaling coefficient =
# circumference of bounding box after transformation applied /
# circumference of bounding box
boundingBoxCircumference = PolygonCircumference([(xa, ya), (xb, ya), (xb, yb), (xa, yb)])
coefficients = [] # list of scaling coefficients
for i in range(m):
    bBox = [IFS(xa, ya, i), IFS(xb, ya, i), IFS(xb, yb, i), IFS(xa, yb, i)]
    coefficients.append(PolygonCircumference(bBox) / boundingBoxCircumference)
    
# Calculate IFS fractal dimension equation value
# if the result is 0 then d is fractal dimension
def IFSfde(d):
    total = 0.0
    for c in coefficients:
        total += c ** d
    return total - 1.0

# Equation Solver using Bisection method
# http://en.wikipedia.org/wiki/Bisection_method
# function values must have opposite signs for f(a) and f(b)
def SolveEq(fun, a, b):
    eps = 1e-7
    ya = fun(a)
    yb = fun(b) 
    y0 = ya
    yc = yb
    while abs(yc - y0) > eps:
        y0 = yc
        c = (a + b) / 2.0
        yc = fun(c)
        if ya * yc < 0:
            b = c
            yb = yc
        elif yb * yc < 0:
            a = c
            ya = yc
        else:
            break
    return c

print "Fractal Name: " + fractalName
print "Scaling Coefficients:"
print coefficients
print "Estimated Fractal Dimension: " + str(SolveEq(IFSfde, 0.0, 3.0))
