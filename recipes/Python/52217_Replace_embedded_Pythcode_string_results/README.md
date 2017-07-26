## Replace embedded Python code in a string with the results of executing that code 
Originally published: 2001-03-09 05:30:56 
Last updated: 2001-03-09 05:30:56 
Author: Joel Gould 
 
This code was originally designed for dynamically creating HTML.  It takes a template, which is a string that may included embedded Python code, and returns another string where any embedded Python is replaced with the results of executing that code.