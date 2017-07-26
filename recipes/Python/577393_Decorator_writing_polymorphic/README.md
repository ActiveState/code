## Decorator for writing polymorphic functions  
Originally published: 2010-09-17 08:57:16  
Last updated: 2010-09-21 06:08:48  
Author: Baptiste Carvello  
  
Python 3 makes a clean separation between unicode text strings (str) and byte
strings (bytes). However, for some tasks (notably networking), it makes sense
to apply the same process to str and bytes, usually relying on the byte string
beeing encoded with an ASCII compatible encoding.

In this context, a polymorphic function is one which will operate on unicode
strings (str) or bytes objects (bytes) depending on the type of the arguments.
The common difficulty is that string constants used in the function also have
to be of the right type. This decorator helps by allowing to use a different
set of constants depending on the type of the argument.