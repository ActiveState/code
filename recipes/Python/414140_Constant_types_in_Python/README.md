## Constant types in Python

Originally published: 2005-05-13 09:08:54
Last updated: 2005-05-15 18:46:12
Author: Ruud Erwig

This is a variation on the existing recipe "Constants in Python" by Alex Martelli. It binds a variable to the type value at first usage. Further usage is then restricted to values of the same type. This avoids a variable of, say, type string to be re-used to contain an integer.