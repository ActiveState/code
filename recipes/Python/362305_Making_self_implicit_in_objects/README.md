## Making self implicit in objectsOriginally published: 2005-01-07 13:18:07 
Last updated: 2005-01-07 13:18:07 
Author: Björn Lindqvist 
 
People used to statically typed languages coming to Python often complain that you have to use "self" (or whichever name you want, but self is most common) to refer to a method or variable in that object. You also have to explicitly pass a reference to the method's object in every call to it. Many people new to Python are annoyed by this and feels that it forces a lot of unnecessary typing. This recipe presents a method which makes "self" implicit.