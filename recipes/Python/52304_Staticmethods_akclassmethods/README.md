## "Static-methods" (aka "class-methods") in Python 
Originally published: 2001-03-26 06:45:43 
Last updated: 2001-06-19 10:16:00 
Author: Alex Martelli 
 
An attribute of a class-object is implicitly mutated into an unbound-method object if it starts out as a Python-coded function; thus, such functions must be wrapped as other callables if "just calling them" (without an instance-argument) is desired.