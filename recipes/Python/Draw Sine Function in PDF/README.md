Created on 2017-08-17

@author: (c) 2017, Jorj X. McKie

License: GNU GPL V3

PyMuPDF Demo Program
---------------------
Create a PDF with drawings of the sine and cosine functions using PyMuPDF.
Depending on how start and end points are located with respect to each
other, horizontal or vertical drawings result.
The vertical case can obviously be used for creating inverse function
(arcus sine / cosine) graphs.

The function graphs are pieced together in 90 degree parts, for which Bezier
curves are used.

Note that the 'alfa' and 'beta' constants represent values for use as 
Bezier control points like so:

* x-values (written in degrees): `[0, 30, 60, 90]`
* corresponding y-values:        `[0, alfa, beta, 1]`

These values have been calculated using the `scipy.interpolate.splrep()` method.
They provide an excellent spline approximation of the sine / cosine
functions - please look at SciPy documentation for background.

