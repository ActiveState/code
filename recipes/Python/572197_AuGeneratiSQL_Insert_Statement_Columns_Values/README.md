## Auto Generation of SQL Insert Statement Columns and Values from Object

Originally published: 2008-05-12 12:27:26
Last updated: 2008-05-12 21:29:06
Author: Andrew Konstantaras

Automates the creation of SQL INSERT statements for the "simple" attributes in a python object by creating a string of an object's attribute names and a corresponding string of that object's attribute values.  Simple attributes are those that are one of the following types: string, int, long, float, boolean, None.