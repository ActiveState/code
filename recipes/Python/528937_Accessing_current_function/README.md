## Accessing current functionOriginally published: 2007-09-09 01:24:19 
Last updated: 2007-09-09 01:24:19 
Author: Arnaud Delobelle 
 
In the body of the function, one sometimes needs to access the function itself (for recursive calls or function attribute access).  Using the function name doesn't work if it is bound to another object later.\n\nThis recipe introduces a 'bindfunction' decorator addressing this.