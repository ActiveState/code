## Integer square root function 
Originally published: 2011-08-04 05:29:16 
Last updated: 2011-08-04 05:29:16 
Author: Steven D'Aprano 
 
The *integer square root* function, or isqrt, is equivalent to floor(sqrt(x)) for non-negative x. For small x, the most convenient way to calculate isqrt is by calling int(x**0.5) or int(math.sqrt(x)), but if x is a large enough integer, the sqrt calculation overflows.\n\nYou can calculate the isqrt without any floating point maths, using just pure integer maths, allowing the function to operate with numbers far larger than possible with floats:\n\n    >>> n = 1234567*(10**1000)\n    >>> n2 = n*n\n    >>> math.sqrt(n2)\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n    OverflowError: long int too large to convert to float\n    >>> isqrt(n2) == n\n    True\n\n