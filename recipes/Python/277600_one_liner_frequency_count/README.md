## one liner frequency countOriginally published: 2004-04-11 00:52:35 
Last updated: 2006-11-17 01:07:04 
Author: Jason Whitlark 
 
You often see frequency counts done with dicts, requiring serveral lines of code.  Here is a way to do it in one line using itertools and list comprehensions.  This revised version was suggested by Raymon Hettinger.  It is O(n log n).