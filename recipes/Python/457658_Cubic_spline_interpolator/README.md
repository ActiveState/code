###Cubic spline interpolator

Originally published: 2005-11-23 09:52:34
Last updated: 2005-11-23 09:52:34
Author: Will Ware

Accepts a function to be approximated, and a list of x coordinates that are endpoints of interpolation intervals. Generates cubic splines matching the values and slopes at the ends of the intervals. Can generate fairly fast C code, or can be used directly in Python.