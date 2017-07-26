## Auto differentiation 
Originally published: 2016-02-18 06:32:10 
Last updated: 2016-08-07 22:02:10 
Author: Raymond Hettinger 
 
Directly computes derivatives from ordinary Python functions using auto differentiation.  The technique directly computes the desired derivatives to full precision without resorting to symbolic math and without making estimates bases on numerical methods.\n\nThe module provides a Num class for "dual" numbers that performs both regular floating point math on a value and its derivative at the same time.  In addition, the module provides drop-in substitutes for most of the functions in the math module.  There are also tools for partial derivatives, directional derivatives, gradients of scalar fields, and the curl and divergence of vector fields.