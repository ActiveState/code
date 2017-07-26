def approx1(c, maxd):
    'Slow way using sequential search'
    d = min(xrange(2, maxd), key=lambda d: abs(round(c*d)/d/c-1))
    return int(round(c*d)), d

import fractions              # Available in Py2.6 and Py3.0

def approx2(c, maxd):
    'Fast way using continued fractions'
    return fractions.Fraction.from_float(c).limit_denominator(maxd)



if __name__ == '__main__':
    import math
    for x in (math.pi, math.e):
        for d in (10, 100, 1000, 10000, 100000, 1000000):
            print approx1(x, d), approx2(x, d)
        print

##### Sample output
        
(22, 7) 22/7
(311, 99) 311/99
(355, 113) 355/113
(355, 113) 355/113
(312689, 99532) 312689/99532
(3126535, 995207) 3126535/995207
        
(19, 7) 19/7
(193, 71) 193/71
(1457, 536) 1457/536
(25946, 9545) 25946/9545
(271801, 99990) 271801/99990
(1084483, 398959) 1084483/398959
