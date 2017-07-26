## Flexible datetime parsingOriginally published: 2012-08-21 07:35:34 
Last updated: 2012-08-21 07:35:34 
Author: Glenn Hutchings 
 
The strptime() method of datetime accepts a format string that you have to specify in advance.  What if you want to be more flexible in the kinds of date your program accepts?  Here's a recipe for a function that tries many different formats until it finds one that works.\n