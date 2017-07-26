## automatically upgrade class instances on reload() 
Originally published: 2002-10-31 07:45:20 
Last updated: 2004-10-27 16:51:20 
Author: Michael Hudson 
 
Anyone who's used reload() on a module that defines a class in the interactive interpreter must have experienced the frustration of then running around and making sure that all instances are updated to be instances of the new rather than the old class.\n\nThis metaclass tries to help with this.