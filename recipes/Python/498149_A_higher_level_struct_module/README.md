## A higher level struct module  
Originally published: 2006-09-30 03:47:36  
Last updated: 2006-10-26 14:47:57  
Author: Brian McErlean  
  
This recipe provides a higher level wrapper around the struct module.  It provides a more convenient syntax for defining and using structs, and adds additional features such as:
  - Allows embedding structures within other structures
  - Allows defining arrays of items (or other structures)
  - Class based syntax, allowing access and updates by field name, not position
  - Extension of structures by inheritance