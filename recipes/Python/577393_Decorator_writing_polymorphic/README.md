## Decorator for writing polymorphic functions 
Originally published: 2010-09-17 08:57:16 
Last updated: 2010-09-21 06:08:48 
Author: Baptiste Carvello 
 
Python 3 makes a clean separation between unicode text strings (str) and byte\nstrings (bytes). However, for some tasks (notably networking), it makes sense\nto apply the same process to str and bytes, usually relying on the byte string\nbeeing encoded with an ASCII compatible encoding.\n\nIn this context, a polymorphic function is one which will operate on unicode\nstrings (str) or bytes objects (bytes) depending on the type of the arguments.\nThe common difficulty is that string constants used in the function also have\nto be of the right type. This decorator helps by allowing to use a different\nset of constants depending on the type of the argument.