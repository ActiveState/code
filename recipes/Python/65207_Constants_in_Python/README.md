## Constants in PythonOriginally published: 2001-06-14 12:37:15 
Last updated: 2001-08-20 07:12:14 
Author: Alex Martelli 
 
In Python, any variable can be re-bound at will -- and modules don't let you define special methods such as an instance's __setattr__ to stop attribute re-binding.  Easy solution (in Python 2.1 and up): use an instance as "module"...