# Complex Polynomial Roots Fractal
# See: Scientific American Magazine, May 2003, "A Digital Slice of Pi"
# FB - 201109051
import math
import random
import time
from PIL import Image
imgx = 512
imgy = 512
image = Image.new("RGB", (imgx, imgy))
# drawing area
xa = -2.0
xb = 2.0
ya = -2.0
yb = 2.0

nmax = 18 # max polynomial degree allowed
pmax = 20000 # max number of polynomials to find roots for
maxIt = 1000 # cutoff for iteration

def polynomial(z, coefficients): # Horner scheme
    t = complex(0, 0)
    for c in reversed(coefficients):
        t = t * z + c
    return t

# Durand-Kerner method for solving polynomial equations
eps = 1e-7 # max error allowed
def DurandKerner(coefficients):
    n = len(coefficients) - 1
    roots = [complex(0, 0)] * n
    for k in range(n):
        roots[k] = complex(random.random(), random.random())
    rootsNew = roots[:]
    flag = True
    it = 0 # number of iterations
    while flag:
        flag = False
        for k in range(n):
            temp = complex(1, 0)
            for j in range(n):
                if j != k:
                    temp *= roots[k] - roots[j]
            rootsNew[k] = roots[k] - polynomial(roots[k], coefficients) / temp
            if abs(roots[k] - rootsNew[k]) > eps:
                flag = True
        roots = rootsNew[:]
        it += 1
        if it > maxIt:
            flag = False
    return (roots, it)

st = time.time()
for p in range(pmax):
    pd = random.randint(2, nmax)
    coefficients = [complex(0, 0)] * (pd + 1)
    for k in range(pd):
        coefficients[k] = complex(math.copysign(1.0, random.randint(0, 1) * 2 - 1), 0) 
    (roots, i) = DurandKerner(coefficients)
    for k in range(len(roots)):
        kx = (imgx - 1) * (roots[k].real - xa) / (xb - xa)
        ky = (imgy - 1) * (roots[k].imag - ya) / (yb - ya)
        if kx >= 0 and kx <= imgx -1 and ky >= 0 and ky <= imgy - 1:
            image.putpixel((int(kx), int(ky)), (i % 8 * 32, i % 4 * 64, i % 16 * 16))
image.save("ComplexPolynomialRootsFractal.png", "PNG")
print "Duration in seconds: " + str(int(time.time() - st))
