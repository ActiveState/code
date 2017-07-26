# IFS fractals w/ automatic probability distribution
# http://en.wikipedia.org/wiki/Iterated_function_system
# http://en.wikipedia.org/wiki/Chaos_game
# FB - 20120311
import random
from PIL import Image
imgx = 512
imgy = 512 # will be auto-re-adjusted according to aspect ratio of the fractal
maxIt = imgx * imgy * 2

##fractalName = "Barnsley Fern"
##mat=[[0.0, 0.0, 0.0, 0.16, 0.0, 0.0],
##     [0.85, 0.04, -0.04, 0.85, 0.0, 1.6],
##     [0.2, -0.26, 0.23, 0.22, 0.0, 1.6],
##     [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44]]

fractalName = "Centipede"
mat = [[0.824074, 0.281482, -0.212346,  0.864198, -1.882290, -0.110607],
       [0.088272, 0.520988, -0.463889, -0.377778,  0.785360,  8.095795]]

##fractalName = "Levy C curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0],
##       [0.5, 0.5, -0.5, 0.5, 0.5, 0.5]]

##fractalName = "Dragon curve"
##mat = [[0.5, -0.5, 0.5, 0.5, 0.0, 0.0],
##       [-0.5, -0.5, 0.5, -0.5, 1.0, 0.0]]

##fractalName = "Sierpinski Triangle"
##mat = [[0.5, 0.0, 0.0, 0.5, 0.0, 0.0],
##       [0.5, 0.0, 0.0, 0.5, 0.5, 0.0],
##       [0.5, 0.0, 0.0, 0.5, 0.0, 0.5]]

# Area of Polygon using Shoelace formula
# http://en.wikipedia.org/wiki/Shoelace_formula
# corners must be ordered in clockwise or counter-clockwise direction
def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def IFS(x, y, i): # apply ith transformation to given point
    x0 = x * mat[i][0] + y * mat[i][1] + mat[i][4] 
    y  = x * mat[i][2] + y * mat[i][3] + mat[i][5] 
    x = x0
    return (x, y)

m = len(mat) # number of IFS transformations

# calculate probabilities of the transformations
areas = [] # areas of transformed rectangles
for j in range(m):
    area = PolygonArea([IFS(1, 1, j), IFS(-1, 1, j), IFS(-1, -1, j), IFS(1, -1, j)])
    areas.append(area)
totalArea = sum(areas)
pArr = []
for j in range(m):
    pArr.append(areas[j] / totalArea)
     
# find bounding rectangle of the fractal using Chaos Game algorithm
x = mat[0][4]
y = mat[0][5] 
xa = x
xb = x
ya = y
yb = y
for k in range(maxIt):
    i = random.randint(0, m - 1)
    if random.random() <= pArr[i]:
        (x, y) = IFS(x, y, i)
        if x < xa:
            xa = x
        if x > xb:
            xb = x
        if y < ya:
            ya = y
        if y > yb:
            yb = y

imgy = int(imgy * (yb - ya) / (xb - xa)) # re-adjust the aspect ratio 
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()

# drawing using Chaos Game algorithm
theColor = (255, 255, 255)
x=0.0
y=0.0 
for k in range(maxIt):
    i = random.randint(0, m - 1)
    if random.random() <= pArr[i]:
        (x, y) = IFS(x, y, i)
        jx = int((x - xa) / (xb - xa) * (imgx - 1)) 
        jy = (imgy - 1) - int((y - ya) / (yb - ya) * (imgy - 1))
        if jx >= 0 and jx < imgx and jy >= 0 and jy < imgy:
            pixels[jx, jy] = theColor
image.save(fractalName + " fractal.png", "PNG")
print "Fractal Name: " + fractalName
print "Probabilities: " + str(pArr)
