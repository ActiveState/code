## mergeable_dict  
Originally published: 2008-08-31 22:25:47  
Last updated: 2008-08-31 22:25:47  
Author: Jérôme Lovy  
  
A very simple specialization of the dictionary that makes it possible to merge two dictionaries provided that they are *compatible* : if a given key is present in both dictionaries, it must be associated with the same value.\n\nThe method is_compatible_with() allows to check this compatibility.\n\nIf possible, dictionaries can then be merged with the merge() method or with the '|' operator. Moreover, '|=' is defined as syntactical sugar for the merge() method.