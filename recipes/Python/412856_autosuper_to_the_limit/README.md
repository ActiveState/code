## autosuper to the limit 
Originally published: 2005-05-01 13:24:31 
Last updated: 2005-05-01 20:27:44 
Author: Diego Novella 
 
This recipe comes from an idea to "improve" Tim Delaney's "autosuper" recipe (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/286195) by using a similar approach but with no need to inherit a class from 'autosuper'. It is now a free function to be used inside a method body whithout the need to pass it the 'self' object:\nclass C(object):\n   def foo(self,*a,**k):\n      # do something\n      autosuper(*a,**k)\n      # do something