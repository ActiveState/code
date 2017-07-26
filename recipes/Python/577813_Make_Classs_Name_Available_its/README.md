## Make a Class's Name Available in its Definition Body 
Originally published: 2011-07-31 03:20:47 
Last updated: 2011-08-04 21:38:40 
Author: Eric Snow 
 
Since a class object is created *after* the body is executed, it can't be available to the class body.  Even the name is unavailable, at least by default.  However, you can use the `__prepare__()` method in a metaclass to stick it in there.  This recipe is a simple demonstration of how.