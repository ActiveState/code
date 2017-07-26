## To 'return None' from your Python-callable C function  
Originally published: 2001-03-26 12:02:44  
Last updated: 2001-03-26 12:02:44  
Author: Alex Martelli  
  
Often a function written in C for Python needs to return nothing in particular -- a "return None" in Python terms; but _don't_ just "return Py_None" from C, as that will mess up reference counts!