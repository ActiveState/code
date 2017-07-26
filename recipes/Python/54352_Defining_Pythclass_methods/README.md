## Defining Python class methods in C

Originally published: 2001-04-25 10:22:15
Last updated: 2001-04-25 10:22:15
Author: Brent Burley

This recipe shows how to define a new Python class from a C extension module.  The class methods are implemented\nin C, but the class can still be instantiated, extended, subclassed, etc. from Python.  The same technique can also\nbe used to extend an existing Python class with methods written in C.