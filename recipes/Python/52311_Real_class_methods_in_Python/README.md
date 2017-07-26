## "Real" class methods in Python  
Originally published: 2001-03-27 11:40:20  
Last updated: 2001-03-27 11:40:20  
Author: Thomas Heller  
  
This recipe demonstrates 'real' class methods, like they are known from Smalltalk.

Class methods implicitely receive the actual class as the first parameter.

They are inherited by subclasses, and may as well be overridden.

Class methods may return anything, although they are particularly useful as constructors.