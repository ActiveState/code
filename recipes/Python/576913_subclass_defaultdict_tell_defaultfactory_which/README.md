## subclass defaultdict to tell default_factory which key is missing  
Originally published: 2009-09-27 11:43:34  
Last updated: 2009-09-27 12:15:27  
Author: Mick Krippendorf  
  
In a little Prolog interpreter I'm writing I needed a simple and concise way to create Var-objects and also store them in a mapping *varname* -> *Var-object* representing the scope of the current Prolog rule. Also, anonymous Prolog variables ("_") should not go into the mapping and should be renamed to *_<unique-number>*. I came up with this: