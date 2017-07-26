###Docstring inheritance decorator

Originally published: 2009-07-28 13:42:32
Last updated: 2009-07-28 13:42:32
Author: Shai Berger

In many cases, a subclass overrides a method in a parent class, just to change its implementation; in such cases, it would be nice to preserve the overridden method's docstring. The decorator below can be used to achieve this without explicit reference to the parent class. It does this by replacing the function with a descriptor, which accesses the parent class when the method is accessed as an attribute.