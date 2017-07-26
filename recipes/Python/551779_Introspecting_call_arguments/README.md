## Introspecting call arguments  
Originally published: 2008-03-18 22:25:57  
Last updated: 2009-05-10 11:32:18  
Author: George Sakkis  
  
This recipe implements in pure Python the algorithm used by the interpreter for binding the values passed as parameters in a function call to the formal arguments of the function.

This is useful for decorators that want to take into account this binding when wrapping a function (e.g. for type checking).

Edit (2008/5/10): Added a second returned value, missing_args: a tuple of the formal parameters whose value was not provided (i.e. those using the respective default value). This is useful in cases where one want to distinguish f() from f(None) given "def f(x=None):".