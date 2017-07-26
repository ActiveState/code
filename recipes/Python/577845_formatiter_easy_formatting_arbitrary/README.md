## format_iter: easy formatting of arbitrary iterables 
Originally published: 2011-08-16 03:42:00 
Last updated: 2011-08-16 11:44:59 
Author: Nick Coghlan 
 
The ``format_iter`` recipe defines a simple wrapper around ``str.join`` and ``str.format`` that makes it easy to format an arbitrary iterable with a specified format string and item separator.