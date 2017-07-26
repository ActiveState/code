## "Real" class methods in PythonOriginally published: 2001-03-27 11:40:20 
Last updated: 2001-03-27 11:40:20 
Author: Thomas Heller 
 
This recipe demonstrates 'real' class methods, like they are known from Smalltalk.\n\nClass methods implicitely receive the actual class as the first parameter.\n\nThey are inherited by subclasses, and may as well be overridden.\n\nClass methods may return anything, although they are particularly useful as constructors.