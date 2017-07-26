## Nested contexts -- a chain of mapping objects 
Originally published: 2010-10-21 08:38:58 
Last updated: 2010-10-25 02:13:37 
Author: Raymond Hettinger 
 
Easy to use chain of dictionaries for crafting nested scopes or for a tree of scopes.  Useful for analyzing AST nodes, XML nodes or other structures with multiple scopes.  Can emulate various chaining styles including static/lexical scoping, dynamic scoping and Python's own globals(), locals(), nested scopes, and writeable nonlocals.  Can also model Python's inheritance chains: instance dictionary, class dictionary, and base classes.