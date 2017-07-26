# Generalized Apollonian Gasket Fractal
# http://en.wikipedia.org/wiki/Apollonian_Gasket
# http://en.wikipedia.org/wiki/Descartes'_theorem
# http://en.wikibooks.org/wiki/Fractals/Apollonian_fractals
# FB - 20120131
import math
import cmath
import random
from PIL import Image, ImageDraw
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
draw = ImageDraw.Draw(image)
maxIt = 2000 # of iterations
n = random.randint(2, 7) # of main circles > 1
print 'Number of main circles: ' + str(n)

eps = 0.0001
def appEq(u, v): # approximately equal excluding signs
    return abs(abs(u) - abs(v)) <= eps

# test if 2 circles are approximately equal
def appEqCir(a, b):
    return (abs(a[0] - b[0]) <= eps and appEq(a[1], b[1]))

# test if 2 circles are tangent
def isTanCir(a, b):
    return (appEq(a[0] - b[0], abs(a[1]) + abs(b[1])) or appEq(a[0] - b[0], abs(a[1]) - abs(b[1])))

# test if 2 circles are intersecting
def isIntCir(a, b):
    dist = abs(a[0] - b[0]) # distance between 2 centers
    rmin = min(abs(a[1]), abs(b[1])) # min radius
    rmax = max(abs(a[1]), abs(b[1])) # max radius
    return (dist + eps < rmin + rmax and dist + rmin > rmax + eps)

# test if 3 circles are tangent to each other
def isTangent(a, b, c):
    flag = True
    if appEqCir(a, b) or appEqCir(a, c) or appEqCir(b, c): # all circles must be different
        flag = False
    if not isTanCir(a, b):
        flag = False
    if not isTanCir(a, c):
        flag = False
    if not isTanCir(b, c):
        flag = False
    return flag

# test if the 4th circle is tangent to previous 3
def isTan4(a, b, c, d):
    return isTangent(a, b, d) and isTangent(a, c, d) and isTangent(b, c, d)

# input: 3 circles w/ each as a tuple: (complex(x,y),r)
# output: 4 tangent circles as a tuple
def cif(a, b, c):
    # curvatures of the circles
    k1 = 1.0 / a[1]
    k2 = 1.0 / b[1]
    k3 = 1.0 / c[1]
    # curvatures of tangent circles
    temp0 = 2.0 * math.sqrt(k1 * k2 + k1 * k3 + k2 * k3)
    temp1 = k1 + k2 + k3
    k40 = temp1 + temp0
    k41 = temp1 - temp0
    # centers of tangent circles
    temp0 = 2.0 * cmath.sqrt(k1*k2*a[0]*b[0]+k1*k3*a[0]*c[0]+k2*k3*b[0]*c[0])
    temp1 = k1 * a[0] + k2 * b[0] + k3 * c[0]
    c40 = (temp1 + temp0) / k40
    c41 = (temp1 - temp0) / k41
    c42 = (temp1 - temp0) / k40
    c43 = (temp1 + temp0) / k41
    # radius of tangent circles
    r0 = 1.0 / k40
    r1 = 1.0 / k41
    # there are 4 solutions and only 2 are correct (tangent) circles
    # those are c0 and c1 or c2 and c3
    c0 = (c40, r0)
    c1 = (c41, r1)
    c2 = (c42, r0)
    c3 = (c43, r1)
    if isTan4(a, b, c, c0) and isTan4(a, b, c, c1):
        return (c0, c1)
    else:
        return (c2, c3)

# pixel coordinate calculation
def pxy(x, y):
    kx = int((x - xa) / (xb - xa) * (imgx - 1))
    ky = int((y - ya) / (yb - ya) * (imgy - 1))
    return (kx, ky)   

# generate the main circles: n circles in a circle
circles = []
a = 2.0 * math.pi / n
# radius of the inner circles
r = math.hypot(math.cos(a) - math.cos(0), math.sin(a) - math.sin(0)) / 2.0
r0 = 1.0 + r # radius of the outer circle
r1 = r0 - 2.0 * r # radius of the center circle
# origin
ox = r0
oy = r0
rmin = 2.0 * r0 / math.hypot(imgx, imgy) # min radius that can be drawn
# drawing area
xa = ox - r0
xb = ox + r0
ya = oy - r0
yb = oy + r0

circles.append((complex(ox, oy), -r0)) # add the outer circle w/ - curvature
for j in range(n): # add the main circles
    cx = math.cos(a * j) + ox
    cy = math.sin(a * j) + oy
    circles.append((complex(cx, cy), r))
if r1 > rmin: # if possible add a center circle
    circles.append((complex(ox, oy), r1))    

p0 = 0
for i in range(maxIt):
    p = int(100 * i / (maxIt - 1))
    if p > p0:
        p0 = p
        print "%" + str(p)
    # randomly select 3 circles
    while True:
        a = random.choice(circles)
        b = random.choice(circles)
        c = random.choice(circles)
        # test if all 3 circles are tangent to each other
        if isTangent(a, b, c): 
            break
    # find inversion circles
    d = cif(a, b, c)
    for e in d:
        dx = e[0].real
        dy = e[0].imag
        dr = e[1]
        # ignore the outer circle (- curvature) solutions and too small circles
        if dx > 0.0 and dy > 0.0 and dr > rmin:
            # add the new circle if it was not added before and not intersecting
            flag = True
            for cir in circles:
                # new circle must not be equal/intersecting to any existing circle
                if appEqCir(cir, e) or isIntCir(cir, e):
                    flag = False
                    break
            if flag:
                circles.append(e)

# draw all circles
for cir in circles:
    dx = cir[0].real
    dy = cir[0].imag
    dr = abs(cir[1])
    try:
        draw.ellipse((pxy(dx - dr, dy - dr), pxy(dx + dr, dy + dr)))
    except:
        pass
image.save("ApollonianGasket_" + str(n) + ".png", "PNG")
