## Remove duplicates from a sequence 
Originally published: 2001-04-06 00:54:02 
Last updated: 2001-04-06 00:54:02 
Author: Tim Peters 
 
The fastest way to remove duplicates from a sequence depends on some pretty subtle properties of the sequence elements, such as whether they're hashable, and whether they support full comparisons.  The unique() function tries three methods, from fastest to slowest, letting runtime exceptions pick the best method available for the sequence at hand.