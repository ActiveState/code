## Print an object only a limited number of times  
Originally published: 2012-12-09 19:41:19  
Last updated: 2012-12-09 19:41:20  
Author: Filippo Squillace  
  
The psome function detects the position into the source files where the
function itself is called. It prints the object according a counter variable.
Therefore, whenever the psome function is called inside a loop the object will
be printed only a limited number of times. This can useful for debugging
code in particular when the data structure we want to scan is quite big and we
want to print only the first elements of it.