## Simplified attribute accessors using overloading  
Originally published: 2003-08-17 00:57:14  
Last updated: 2003-08-17 00:57:14  
Author: Ulrich Hoffmann  
  
This recipe presents an ideom for simplified accessors, that combines
typical getter and setter functionality of an attribute into a single
overloaded method, that instead of getATTRIBUTE and setATTRIBUTE can
now just be called ATTRIBUTE. When called without arguments it acts as
a getter and retrieves the attribute's value. When called with
arguments, the attribute is set to this value.

Uses a neat trick of an exclusive unique value in default arguments.