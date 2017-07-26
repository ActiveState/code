## where() function for generator expressions (Python 3)  
Originally published: 2014-10-04 18:48:04  
Last updated: 2014-10-05 04:10:21  
Author: Alan Cristhian Ruiz  
  
Function that work like an "where statement" for generator expression. The code below

    x, y, z = 1, 2, 3
    ((x, y, z) for _ in range(5))

Is equivalent to:

    ((x, y, z) for _ in range(5)) < where(x=1, y=2, z=3)