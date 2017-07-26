## Dot-style nested lookups over dictionary based data structures  
Originally published: 2008-12-14 22:30:40  
Last updated: 2008-12-14 14:32:59  
Author: David Moss  
  
This recipe allows you to present dictionary based nested data stuctures in your Python code as objects with nested attributes.

It provides dot ('.') based attribute lookups, like this :-

    >>> x = d.foo.bar.baz

instead of the usual (and longer) Python dictionary syntax lookups :-

    >>> x = d['foo']['bar']['baz']

This recipe saves you *lot* of typing!

For simplicity and readability this particular version show a read only lookup class.