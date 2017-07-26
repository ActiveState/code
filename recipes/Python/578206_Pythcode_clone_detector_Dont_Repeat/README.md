## Python code clone detector (Don't Repeat Yourself)  
Originally published: 2012-07-10 22:34:35  
Last updated: 2012-07-12 14:59:11  
Author: fra   
  
Find duplicate code in Python 2/3 source files. Write a nice report about it.

Works at the Abstract Syntax Tree level, which is a robust way to detect clones.
See this [code duplicated in the Python 3.2 standard library](http://francois.boutines.free.fr/python-3.2-report.html).

**Update**: I cleaned the code a little bit, made it Python 2.7 compatible and faster.