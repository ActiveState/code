###Convex hull and diameter of 2d point sets

Originally published: 2002-03-07 17:56:08
Last updated: 2003-10-16 18:44:57
Author: David Eppstein

Returns the convex hull (separated into upper and lower chains of vertices) and the diameter (farthest pair of points), given input consisting of a list of 2d points represented as pairs (x,y).  The convex hull algorithm is Graham's scan, using a coordinate-based sorted order rather than the more commonly seen radial sorted order.  A rotating calipers algorithm generates candidate pairs of vertices for the diameter calculation.  Care was taken handling tricky cases such as pairs of points with the same x-coordinate and colinear triples of points.