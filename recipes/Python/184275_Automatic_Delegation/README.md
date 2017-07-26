## Automatic Delegation  
Originally published: 2003-02-24 07:25:24  
Last updated: 2003-02-24 15:31:44  
Author: Atsushi Odagiri  
  
Delegation gives us monotonous codings.\nBut, special method '__getattr__' is called when a certain object does  not have the called method.\n\nThis recipe solve the tiresome coding.\nThe object should call delegated object's method by argument 'name'.