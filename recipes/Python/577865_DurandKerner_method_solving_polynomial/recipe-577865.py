# Durand-Kerner method for solving polynomial equations
# http://en.wikipedia.org/wiki/Durand%E2%80%93Kerner_method
# http://en.wikipedia.org/wiki/Horner%27s_method
# http://en.wikipedia.org/wiki/Properties_of_polynomial_roots
# FB - 20130428
import random
import math

def bound(coefficients):
    coefficients.reverse()
    n = len(coefficients) - 1
    b = 0.0
    for i in range(n):
        b += abs(coefficients[i] / coefficients[i + 1])   
    coefficients.reverse()
    return b

def polynomial(z, coefficients): # Horner method
    t = complex(0, 0)
    for c in reversed(coefficients):
        t = t * z + c
    return t

eps = 1e-7 # max error allowed
def DurandKerner(coefficients):
    n = len(coefficients) - 1
    roots = [complex(0, 0)] * n
    bnd = bound(coefficients)
    retry = True
    while retry:
        retry = False
        # set initial roots as random points within bounding circle
        for k in range(n):
            r = bnd * random.random()
            theta = 2.0 * math.pi * random.random()
            roots[k] = complex(r * math.cos(theta), r * math.sin(theta))

        itCtr = 0
        rootsNew = roots[:]
        flag = True
        while flag:
            flag = False
            for k in range(n):
                temp = complex(1.0, 0.0)
                for j in range(n):
                    if j != k:
                        temp *= roots[k] - roots[j]
                rootsNew[k] = roots[k] - polynomial(roots[k], coefficients) / temp
                if abs(roots[k] - rootsNew[k]) > eps:
                    # print abs(roots[k] - rootsNew[k])
                    flag = True
                if math.isnan(rootsNew[k].real) or math.isnan(rootsNew[k].imag):
                    flag = False
                    retry = True
                    print 'retrying...'
                    break
            roots = rootsNew[:]
            itCtr += 1

    print "iteration count: " + str(itCtr)
    return roots

# example
# x**3-3*x**2+3*x-5=0
coefficients = [complex(-5, 0), complex(3, 0), complex(-3, 0), complex(1, 0)]
print "coefficients: " + str(coefficients)
print "roots: " + str(DurandKerner(coefficients))
