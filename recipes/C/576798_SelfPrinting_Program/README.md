## Self-Printing Program 
Originally published: 2009-06-05 01:19:17 
Last updated: 2009-06-05 01:19:17 
Author: J Y 
 
The two key tricks here are using a string with an embedded %s specifier to allow the string to contain itself when printed, and to use the %c format specifier to allow printing out special characters like newlines, which could not otherwise be embedded in the output string. 