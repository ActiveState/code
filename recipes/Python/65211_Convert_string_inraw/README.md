## Convert a string into a raw string  
Originally published: 2001-06-14 21:08:49  
Last updated: 2001-06-19 00:18:59  
Author: Brett Cannon  
  
This function takes in an arbitrary string and converts it into its raw string equivalent.  Unfortunately \x will raise a ValueError and I cannot figure out how to deal with it.

[2001-06-18: Completely reworked function for performance]