## affinity.py  
Originally published: 2012-06-05 02:41:03  
Last updated: 2012-06-05 03:12:55  
Author: Stephen Chappell  
  
Allow a simple way to ensure execution is confined to one thread.

This module defines the Affinity data type that runs code on a single thread.
An instance of the class will execute functions only on the thread that made
the object in the first place. The class is useful in a GUI's main loop.