## Exception handling in a single line

Originally published: 2009-08-09 10:25:58
Last updated: 2009-10-09 01:07:52
Author: Radek Szklarczyk

The rules of *duck typing* in python encourage programmers to use the "try...except..." clause. At the same time python with new versions enables to use more powerful list comprehensions (for example Conditional Expressions). However, it is impossible to write the "try...except..." clause in a list comprehension. The following recipe "protects" a function against exception and returns a default value in the case when exception is thrown.