## sparse: A dictionary based sparse matrix classOriginally published: 2001-03-16 08:02:38 
Last updated: 2005-04-18 00:17:29 
Author: Alexander Pletzer 
 
'sparse' is a matrix class based on a dictionary to store data using 2-element tuples (i,j)\n as keys (i is the row and j the column index). The common matrix operations such as\n'dot' for the inner product, multiplication/division by a scalar, indexing/slicing, etc. are\noverloaded for convenience. When used in conjunction with the 'vector' class, 'dot'\nproducts also apply between matrics and vectors. Two methods, 'CGsolve' and\n'biCGsolve', are provided to solve linear systems. Tested using Python 2.2.