"""\
<<Your current doc-string goes here.>>

Note:  The following doctest verifies that we're exporting all of the
symbols that we're supposed to be.  First, we gather all of the
symbols imported using 'from X import *'. Next we look at our global
name-space, discarding those we definitely don't want and then only
keeping those that meet our criteria.  Finally, we print the differences
between what we found and what's actually being exported.

>>> from new import classobj
>>> exclusions = set()
>>> for name in ['Tkinter']:
...     exclusions.update(dir(__import__(name)))
>>> exports = set()
>>> namespace = globals().copy()
>>> for name in namespace:
...     if name in exclusions or name.startswith("_"):
...         pass
...     else:
...         if name == name.upper():
...             exports.add(name)
...         elif name.endswith('Icon'):
...             exports.add(name)
...         elif isinstance(namespace[name], classobj):
...             exports.add(name)
...         else:
...             pass

>>> print "Missing from __all__:", sorted(exports - set(__all__))
Missing from __all__: []

>>> print "Extraneous in __all__:", sorted(set(__all__) - exports)
Extraneous in __all__: []

"""

__all__ = []

<<Your module's code goes here.>>

if __name__ == '__main__':
    import doctest
    doctest.testmod()
