from pylab import *
from scipy import e
x = arange(0, 15, 0.001)
print x
energy_spectrum_distribution = (pow(x,3)/pow(e,x)-1)
title('The energy density distribution')
plot(x,energy_spectrum_distribution)
show()
