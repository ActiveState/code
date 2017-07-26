## Generate field name to column number dictionary 
Originally published: 2001-03-21 11:05:52 
Last updated: 2001-03-21 11:05:52 
Author: Tom Jenkins 
 
When you get a set of rows from a cursor.fetch[one, many, all] call, it is sometimes helpful to be able to access a specific column in a row by the field name and not the column number.  This function takes a DB API 2.0 cursor object and returns a dictionary with column numbers keyed to field names.