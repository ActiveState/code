## function composition 
Originally published: 2001-04-17 22:31:28 
Last updated: 2001-04-17 22:31:28 
Author: Scott David Daniels 
 
These two classes show two styles of function composition.  The\ndifference is only when the second function (g) returns a tuple.\ncompose passes the results of g as a tuple, mcompose treats it as\na tuple of args to pass along.  Note that extra args provided to\n(m)compose are treated as extra args to f (there is no standard\nfunctional behavior here to follow).\n\n    compose(f,g, x...)(y...) = f(g(y...), x...)\n   mcompose(f,g, x...)(y...) = f(*g(y...), x...)