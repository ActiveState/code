## Approximately EqualOriginally published: 2010-03-17 17:05:50 
Last updated: 2010-03-17 17:05:51 
Author: Steven D'Aprano 
 
Generic "approximately equal" function for any object type, with customisable error tolerance.\n\nWhen called with float arguments, approx_equal(x, y[, tol[, rel]) compares x and y numerically, and returns True if y is within either absolute error tol or relative error rel of x, otherwise return False. The function defaults to sensible default values for tol and rel.\n\nFor any other pair of objects, approx_equal() looks for a method __approx_equal__ and, if found, calls it with arbitrary optional arguments. This allows types to define their own concept of "close enough".\n