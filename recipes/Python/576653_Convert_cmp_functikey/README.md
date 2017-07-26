## Convert a cmp function to a key functionOriginally published: 2009-02-18 22:40:14 
Last updated: 2010-04-04 23:28:40 
Author: Raymond Hettinger 
 
Py3.0 transition aid.  The *sorted()* builtin and the *list.sort()* method no longer accept a *cmp* function in Python 3.0.  Most cases are easy to convert manually.  This recipe handles the remaining cases.