## Delphi-like property class for Python 2.2

Originally published: 2002-01-28 10:07:35
Last updated: 2002-01-28 10:07:35
Author: Yakov Markovitch

"property", a very nice new Python 2.2 feature that allows to specify per-attribute access logic, has one drawback: it requires to specify attribute access functions (fget and/or fset) even if direct access to the attribute is needed (the case when f.i. only setting the attribute must be controlled but getting can be performed directly). There is an excellent solution for this problem in systems like Delphi or Borland C++ Builder: a programmer can specify the name of a member variable as a getter and/or setter of a property, in which case corresponding property access goes directly to that member variable.\nHere is a proposed solution for Python: