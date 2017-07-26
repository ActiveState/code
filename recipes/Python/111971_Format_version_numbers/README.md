## Format version numbers  
Originally published: 2002-02-04 14:09:35  
Last updated: 2002-02-04 14:09:35  
Author: Tim Keating  
  
It is common for Python modules to export their version number in list or tuple form. While it is simple to convert a dot-delimited string to a tuple, it's subtle and tricky to go the other way, particularly when you don't know how many "digits" there are. This recipe includes a pair of functions that convert between forms. Also handy for IP addresses!