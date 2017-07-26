## Flipdict -- python dict that also maintains a one-to-one inverse mapping 
Originally published: 2009-11-27 09:56:48 
Last updated: 2009-12-03 14:43:52 
Author: Francis Carr 
 
A Flipdict is a python dict subclass that maintains a one-to-one inverse mapping.  Each key maps to a unique value, and each value maps back to that same key.  Each instance has a "flip" attribute to access the inverse mapping.