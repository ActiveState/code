## PyQt4 pressed modifier keys names as method argument by a decorator Originally published: 2013-09-25 15:41:17 
Last updated: 2013-09-29 14:13:04 
Author: TNT  
 
This is a definition of a decorator function that checks which modifier keys are being pressed and adds a keyword argument to a method. This argument is a tuple of names (strings) of the modifier keys that have been pressed when the method was called (or triggered).