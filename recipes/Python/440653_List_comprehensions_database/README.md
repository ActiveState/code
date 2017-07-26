## List comprehensions for database requests  
Originally published: 2005-10-04 12:44:32  
Last updated: 2005-10-04 12:44:32  
Author: Pierre Quentel  
  
The usual way to make a request to a database is to write a string with the SQL syntax, then execute this request and get the result as a list with cursor.fetchall() or cursor.fetchone()

Python has list comprehensions to select items in an iterable if a certain condition is true ; this is very similar to database requests

This recipe wraps a table of a DB-API compliant database in a class that implements the iteration protocol, so that you can use the for ... in ... if ... syntax