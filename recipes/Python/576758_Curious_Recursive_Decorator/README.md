## Curious Recursive Decorator Pattern  
Originally published: 2009-05-16 09:57:26  
Last updated: 2009-05-16 10:00:22  
Author: Y S  
  
There are **no** ABCs for ordering operations.
This is because the recursive class difinition like:

     class Derived(XXX(Derived)):

is invalid syntax. This recipe implements an ABC ordering class with using decorator.