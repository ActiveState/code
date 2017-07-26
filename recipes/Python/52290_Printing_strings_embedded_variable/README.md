## Printing strings with embedded variable names

Originally published: 2001-03-22 14:53:47
Last updated: 2002-06-05 03:41:24
Author: Michael Strasser

This class encapsulates a string with embedded variable names. They are usually evaluated when the object's __str__() method is called. You can specify that they be evaluated when the object is created by including the immediate argument to the constructor. The doc string at the top of the module has an example of its use.\n\nItamar Shtull-Trauring's printexpr.py inspired me to try this out.