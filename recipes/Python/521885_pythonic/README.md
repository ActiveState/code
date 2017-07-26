## A pythonic implementation of xrangeOriginally published: 2007-06-04 18:34:55 
Last updated: 2007-06-04 18:34:55 
Author: Eyal Lotem 
 
The built-in xrange is fast, but it does not support floats and longs as start,stop,step parameters.\nThis means you cannot iterate large number (that don't fit in an int) ranges via xrange as you would with small numbers.