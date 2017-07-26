## Component architecture through data descriptors and function decorators  
Originally published: 2009-07-21 16:21:03  
Last updated: 2009-07-23 11:13:48  
Author: Danny G  
  
My desire was to design a class with defined attributes that when assigned on instances, would expand the instance's functionality.  In other words if I create an instance of class A, then assign a 'component' attribute upon that instance, I should be able to call methods of the component object through the original instance.  I believe this is somewhat similar to interfaces and abstract base classes (and I read up on both a bit), but I want to rely more on introspection of the object to see what it can do versus confining it to a set interface.