from cmath import *

g = 7
lanczos_coef = [ \
     0.99999999999980993,
   676.5203681218851,
 -1259.1392167224028,
   771.32342877765313,
  -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
     9.9843695780195716e-6,
     1.5056327351493116e-7]

def gamma(z):
    z = complex(z)
    if z.real < 0.5:
        return pi / (sin(pi*z)*gamma(1-z))
    else:
        z -= 1
        x = lanczos_coef[0]
        for i in range(1, g+2):
            x += lanczos_coef[i]/(z+i)
        t = z + g + 0.5
        return sqrt(2*pi) * t**(z+0.5) * exp(-t) * x

from pylab import *
        

y = []
x = arange(-4.5, 4.5, 0.1)

for point in x:
   y.append(gamma(point))
      
plot(x, y, 'r-')
axis([-5, 5, -20, 25])
title('gamma plot using lanczos approximation')
grid(True)
savefig('gamma.png')
