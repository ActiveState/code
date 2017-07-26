## Immutable class decorator  
Originally published: 2012-08-05 08:30:40  
Last updated: 2012-08-05 08:30:41  
Author: Oren Tirosh  
  
Apply this decorator to a class with __slots__. Members will be mutable during the execution of __init__ but read-only afterwards.