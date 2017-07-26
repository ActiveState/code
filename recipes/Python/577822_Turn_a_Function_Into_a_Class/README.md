###Turn a Function Into a Class

Originally published: 2011-08-04 05:32:17
Last updated: 2011-10-05 18:38:43
Author: Eric Snow

The only catch is that the function has to return locals() at the end.  And it doesn't do the __prepare__ part of 3.x metaclasses.