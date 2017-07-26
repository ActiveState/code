## A MutableMapping that Can Use Unhashable Objects as Keys  
Originally published: 2012-04-04 20:36:59  
Last updated: 2012-04-04 20:36:59  
Author: Eric Snow  
  
The catch is that the unhashable objects aren't actually stored in the mapping.  Only their IDs are.  Thus you must also store the actual objects somewhere else.