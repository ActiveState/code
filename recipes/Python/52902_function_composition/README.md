## function composition  
Originally published: 2001-04-17 22:31:28  
Last updated: 2001-04-17 22:31:28  
Author: Scott David Daniels  
  
These two classes show two styles of function composition.  The
difference is only when the second function (g) returns a tuple.
compose passes the results of g as a tuple, mcompose treats it as
a tuple of args to pass along.  Note that extra args provided to
(m)compose are treated as extra args to f (there is no standard
functional behavior here to follow).

    compose(f,g, x...)(y...) = f(g(y...), x...)
   mcompose(f,g, x...)(y...) = f(*g(y...), x...)