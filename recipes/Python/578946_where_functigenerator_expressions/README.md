###where() function for generator expressions (Python 3)

Originally published: 2014-10-04 18:48:04
Last updated: 2014-10-05 04:10:21
Author: Alan Cristhian Ruiz

Function that work like an "where statement" for generator expression. The code below\n\n    x, y, z = 1, 2, 3\n    ((x, y, z) for _ in range(5))\n\nIs equivalent to:\n\n    ((x, y, z) for _ in range(5)) < where(x=1, y=2, z=3)