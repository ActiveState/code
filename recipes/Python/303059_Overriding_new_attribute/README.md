## Overriding __new__ for attribute initialization  
Originally published: 2004-09-01 22:42:50  
Last updated: 2004-09-01 22:42:50  
Author: Dan Perl  
  
Whenever a superclass implements a __init__ method to initialize its attributes, subclasses derived from it have to invoke the __init__ method of the superclass.  This recipe is a different mechanism of initializing the attributes of a superclass with default values, achieved by overriding the __new__ method.