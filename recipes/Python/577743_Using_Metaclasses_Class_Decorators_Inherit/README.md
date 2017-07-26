## Using Metaclasses and Class Decorators to Inherit Function DocstringsOriginally published: 2011-06-08 23:31:51 
Last updated: 2011-06-11 00:59:35 
Author: Eric Snow 
 
You'll find three different approaches to copying the method's docstring to the overriding method on a child class.\n\nThe function decorator approach is limited by the fact that you have to know the class when you call the decorator, so it can't be used inside a class body.  However, recipe #577746 provides a function decorator that does not have this limitation.