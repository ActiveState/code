###Simple polynomial class

Originally published: 2009-11-10 11:37:51
Last updated: 2014-02-13 20:55:55
Author: Sam Denton

This implements polynomial functions over a single variable in Python.  It represents the polynomial as a list of numbers and allows most arithmetic operations, using conventional Python syntax.  It does not do symbolic manipulations.  Instead, you can do things like this:\n\n    x = SimplePolynomial()\n    eq = (x-1)*(x*1)\n    print eq     # prints 'X**2 - 1'\n    print eq(4)  # prints 15