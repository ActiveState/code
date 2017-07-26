## Implementing Java inner classes using descriptors  
Originally published: 2005-04-11 11:56:27  
Last updated: 2005-07-08 22:08:04  
Author: George Sakkis  
  
Java programs use extensively "inner" (or nested) classes. There are actually four kinds of such classes (http://www.unix.org.ua/orelly/java-ent/jnut/ch03_08.htm), namely static and non-static member classes, local classes and anonymous inner classes. Python supports directly the last two through classes defined in nested scopes and lambdas. This recipe implements the first two kinds, static and non-static member classes.

A non-static member class is associated with an instance of the outer class and has implicit access to its __dict__. Thus, if the normal attribute lookup fails for an instance of the inner class, it continues to the outer instance.

Similarly, a static member class is associated with the outer class, instead of a specific instance of the outer class.

In both cases, the outer object (instance or class) can be explicitly accessed though the '__outer__' attribute.