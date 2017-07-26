## Starting several context managers concurrently 
Originally published: 2010-08-11 14:27:00 
Last updated: 2010-08-11 14:27:01 
Author: Carlos Valiente 
 
This recipe implements the `parallel` context manager, which executes the `__enter__` and `__exit__` method of its arguments concurrently.