## Track new/unreclaimed objects between 2 points in the codeOriginally published: 2008-10-03 14:13:50 
Last updated: 2008-10-03 12:14:52 
Author: david decotigny 
 
This module provides 3 ways of detecting which objects have been allocated (methods 1 and 3) or became un-reclaimable (method 2) between 2 points in the code. It can be very useful to detect memory leaks (eg. cycles involving objects with a __del__ method).