## vector: A list based vector class supporting elementwise operations 
Originally published: 2001-03-16 07:30:45 
Last updated: 2002-04-15 18:22:16 
Author: Alexander Pletzer 
 
This vector class stores elements in a list and hence allows the 'vector' to grow\ndynamically. Common mathematical functions (sin, cosh, etc) are supported elementwise\nand so are a number of 'external' operations (dot for the inner product between vectors,\nnorm, sum etc.).  This class does not rely on NumPy but can be used in conjunction with\na 'sparse' matrix class to solve linear systems. Tested using Python 2.0 and Jython 2.0.