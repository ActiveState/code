## Readable switch construction without lambdas or dictionaries 
Originally published: 2005-04-25 07:30:27 
Last updated: 2005-04-26 10:51:04 
Author: Brian Beck 
 
Python's lack of a 'switch' statement has garnered much discussion and even a PEP. The most popular substitute uses dictionaries to map cases to functions, which requires lots of defs or lambdas. While the approach shown here may be O(n) for cases, it aims to duplicate C's original 'switch' functionality and structure with reasonable accuracy.