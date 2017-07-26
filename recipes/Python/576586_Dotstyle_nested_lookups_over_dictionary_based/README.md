## Dot-style nested lookups over dictionary based data structuresOriginally published: 2008-12-14 22:30:40 
Last updated: 2008-12-14 14:32:59 
Author: David Moss 
 
This recipe allows you to present dictionary based nested data stuctures in your Python code as objects with nested attributes.\n\nIt provides dot ('.') based attribute lookups, like this :-\n\n    >>> x = d.foo.bar.baz\n\ninstead of the usual (and longer) Python dictionary syntax lookups :-\n\n    >>> x = d['foo']['bar']['baz']\n\nThis recipe saves you *lot* of typing!\n\nFor simplicity and readability this particular version show a read only lookup class.