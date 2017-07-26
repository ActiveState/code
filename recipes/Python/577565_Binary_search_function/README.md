## Binary search function.Originally published: 2011-02-07 05:44:44 
Last updated: 2011-02-07 06:37:52 
Author: Kevin L. Sitze 
 
For a number of years Python has provided developers with the special parameters 'cmp' and 'key' on list.sort and __builtin__.sorted.  However Python does not provide a built-in mechanism for doing binary searches on such sorted lists.  This recipe provides a simple function that allows you to perform binary searches on your sorted sequences.