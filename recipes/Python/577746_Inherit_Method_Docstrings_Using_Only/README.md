## Inherit Method Docstrings Using Only Function Decorators  
Originally published: 2011-06-11 00:52:58  
Last updated: 2011-06-26 02:28:55  
Author: Eric Snow  
  
This recipe provides a descriptor and a decorator.  The decorator will be used on any method in your class to indicate that you want that method to inherit its docstring.

This is useful when you are using abstract bases classes and want a method to have the same docstring as the abstract method it implements.

This recipe uses recipe #577745, the deferred_binder module.