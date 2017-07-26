# Author: Alex Baker
# Description: fixed version of the routine from the web
# Date : 2 Apr 2008

from numpy import *	# for outer and arange
import pylab as p	# for figure
import matplotlib.axes3d as p3	# 3D axes class

fig = p.figure()	
ax = p3.Axes3D(fig)	

theta = arange(0,pi,pi/10)	
phi = arange(0,2*pi,pi/10)	
r = 2 * pow(math.e, -((theta**4)/(0.25**2))) # need to distort the radius by some function

x = r*outer(cos(phi), sin(theta))	
y = r*outer(sin(phi), sin(theta))
z = r*outer(ones(phi.shape), cos(theta))	

print shape(x), shape(y), shape(z)

ax.plot_wireframe(x,y,z)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

p.show()
