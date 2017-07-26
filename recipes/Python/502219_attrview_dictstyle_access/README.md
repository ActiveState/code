## attrview(): dict-style access to attributes 
Originally published: 2007-02-15 19:55:27 
Last updated: 2007-02-21 15:49:08 
Author: Greg Falcon 
 
This class wraps any object, and allows accessing and modifying that object's properties using the dict interface.  This wrapper is meant to provide a clean  interface to getattr/setattr/hasattr/delattr.