## "once" decorator 
Originally published: 2005-06-11 18:12:27 
Last updated: 2005-06-19 00:15:03 
Author: Ori Peleg 
 
This decorator runs a function or method once and caches the result.\n\nIt offers minimal memory use and high speed (only one extra function call). It is _not_ a memoization implementation, the result is cached for all future arguments as well.\n\nThis code is used in the TestOOB testing framework (http://testoob.sourceforge.net).