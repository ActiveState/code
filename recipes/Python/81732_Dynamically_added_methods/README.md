## Dynamically added methods to a class  
Originally published: 2001-10-15 02:49:01  
Last updated: 2001-10-15 02:49:01  
Author: Brett Cannon  
  
Ruby has the functionality of being able to add a method to a class at an arbitrary  point in your code.  I figured Python must have some way for allowing this to happen, and it turned out it did.  The method is available instantly to all already existing instances and of course ones yet to be created.  If you specify method_name then that name is used for the method call.\n\nOne thing to make sure to do is that the function has a variable for the instance to be passed to (i.e. self).