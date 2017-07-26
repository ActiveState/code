###Python Immutable Enumerations Using Duck Punching

Originally published: 2012-10-18 19:41:21
Last updated: 2012-10-18 19:41:22
Author: Josh Friend

Here's a fun method of creating enumerations in Python using dynamic class creation and duck-punching (monkey-patching). It works by creating a class called `enum` using the `type` metaclass. Duck-punching is then used to add properties to the class. the `fget` method of the property returns the enum value, but the `fset` and `fdel` methods throw exceptions, keeping the enumeration immutable. You can have enum values assigned automatically in sequence, assign them yourself, or have a mix of both.