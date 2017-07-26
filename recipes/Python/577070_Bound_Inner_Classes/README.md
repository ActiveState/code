## Bound Inner Classes 
Originally published: 2010-02-24 17:02:57 
Last updated: 2013-12-10 02:36:25 
Author: Larry Hastings 
 
This recipe provides the class decorator `BoundInnerClass`.  The decorator makes inner classes symmetric with method calls.  Functions declared inside classes become "methods", and when you call them through an object they automatically get a reference to "self".  The `BoundInnerClass` decorator makes this work for inner classes: an inner class decorated with `BoundInnerClass` gets a reference to that same (now "outer") object passed in automatically to the inner class's `__init__`.\n\nThe recipe works unchanged in Python 2.6 and 3.1, and is licensed using the Zlib license.