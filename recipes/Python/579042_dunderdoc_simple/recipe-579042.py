"""
dunderdoc.py
A Python function to print the .__doc__ attribute (i.e. the docstring) 
of each item in a list of names given as the argument.
The function is called dunderdoc because it is an informal convention 
in the Python community to call attributes such as __name__, that begin 
and end with a double underscore, dunder-name, and so on.
Author: Vasudev Ram - http://www.dancingbison.com
Copyright 2015 Vasudev Ram
"""

def dunderdoc(names):
    for name in names:
        print '-' * 72
        print name + '.__doc__:'
        print eval(name).__doc__
    print '-' * 72

# Call dunderdoc() on some basic objects:

a = 1 # an integer
b = 'abc' # a string
c = False # a boolean
d = () # a tuple
e = [] # a list
f = {} # a dict
g = set() # a set

dunderdoc(('a', 'b', 'c', 'd', 'e', 'f', 'g'))

# Call dunderdoc() on some user-defined objects:

class Foo(object):
    """
    A class that implements Foo instances.
    """

def bar(args):
    """
    A function that implements bar functionality.
    """

dunderdoc(['Foo', 'bar'])
