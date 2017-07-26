###Validating classes and objects against an Abstract Base Class

Originally published: 2011-05-20 22:38:59
Last updated: 2011-05-21 19:14:19
Author: Eric Snow

Abstract Bases Classes in Python provide great features for describing interfaces programmatically.  By default a subclass is validated against all its ABC parents at instantiation time (in object.__new__).  This recipe aims to provide for validation against an ABC of:\n\n- any class at definition time (including subclasses and registered classes),\n- any object at any time.\n\nI have included an example of the reason I did all this.  It allows you to implement an ABC in the instance rather than the class.\n\nIf the classes argument to validate is None then it tries to build the list of classes from the object's MRO.  If the ABCMeta.register method facilitated an __implements__ list on classes, we could also use that to validate against the registered "base" classes.\n\n\nThe code I have provided is for Python 3, but it should work in 2.7 with a little modification.\n\nThis code borrows from Lib/abc.py and objects/typeobject.c