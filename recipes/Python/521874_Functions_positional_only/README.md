## Functions with positional only arguments.Originally published: 2007-05-31 00:35:09 
Last updated: 2007-05-31 00:35:09 
Author: Arnaud Delobelle 
 
Sometimes it is useful to make sure that arguments in a function are positional only, i.e. cannot be passed as keywords.\nThis recipe defines a decorator 'posonly' that does this: arguments cannot be passed as keywords.  Note that **kwargs can still be used in the function definition to accept keywords.