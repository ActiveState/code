## Class decorator to check that methods are implemented.  
Originally published: 2011-05-27 22:56:45  
Last updated: 2011-05-27 23:52:28  
Author: Jeffrey Fischer  
  
This decorator wraps the class's __init__ function to check that provided set of methods is present on the instantiated class. This is useful for avoiding inheritance in mix-in classes. We can inherit directly from object and still make it clear what methods we expect in other classes to be combined with the mix-in.

Requires at least Python 2.6, which added class decorators.