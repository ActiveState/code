## dualmethod descriptor 
Originally published: 2010-02-04 16:06:33 
Last updated: 2010-02-06 20:54:45 
Author: Steven D'Aprano 
 
This descriptor can be used to decorate methods, similar to the built-ins classmethod and staticmethod. It enables the caller to call methods on either the class or an instance, and the first argument passed to the method will be the class or the instance respectively.\n\nThis differs from classmethods, which always passes the class, and staticmethods, which don't pass either.\n\nLike all descriptors, you can only use this in new-style classes.