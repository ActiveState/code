## Inherit method docstrings without breaking decorators or violating DRY  
Originally published: 2013-06-30 20:09:12  
Last updated: 2013-07-01 02:29:40  
Author: nikratio   
  
There are several recipes for inheriting method docstrings. However, most of them either violate DRY (and have you repeat the ancestor class name in the method decorator that sets the docstring), or do break decorators that try to access the docstring (because the docstring is only assigned after class creation). This recipe avoids both problems.

**Note**: This recipe uses the mro method from http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/