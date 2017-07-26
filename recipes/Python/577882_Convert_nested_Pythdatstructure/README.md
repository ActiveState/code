###Convert a nested Python data structure to XML

Originally published: 2011-09-28 13:14:14
Last updated: 2011-10-17 12:48:59
Author: Graham Poulter

Uses lxml.etree to convert a Python object consisting of nested dicts, tuples, lists, strings and string-convertable objects into a very basic no-attributes, untyped dialect of XML in which elements are named after dictionary keys, and "<i>" is the element for anonymous list and tuple items.\n\nDoes not support: encoding or decoding of strings, invalid floating point values, detection of circular references.