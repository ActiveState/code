## case-insensitive sort of list of stringsOriginally published: 2002-12-19 16:54:05 
Last updated: 2002-12-25 18:29:05 
Author: Kevin Altis 
 
The default compare function used when sorting a list of strings uses the ordinal value of the string characters for comparison. This results in the typical ASCII sort result of 'B' < 'a'. If a user is going to see the list, it is generally better to do a case-insensitive comparison.