###Simulating the ternary operator in Python

Originally published: 2001-03-19 13:06:05
Last updated: 2001-03-19 13:06:05
Author: Jürgen Hermann

People coming from C, C++ or Perl might miss the so-called ternary operator ?: (condition ? then-expr : else-expr). It's most often used for avoiding several lines of code and temporary variables for very simple decisions, like printing the plural form of words after a counter (see example code).\n\nThere are two ways to get the same effect in Python: selecting one of two values from a tuple, or using the special behaviour of the "and" and "or" operators in Python. The second method has the advantage that only ONE of the two possible expressions is evaluated, and is thus more close to the behaviour of ?: as defined by C.