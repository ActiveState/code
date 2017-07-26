## Print an object only a limited number of times  
Originally published: 2012-12-09 19:41:19  
Last updated: 2012-12-09 19:41:20  
Author: Filippo Squillace  
  
The psome function detects the position into the source files where the\nfunction itself is called. It prints the object according a counter variable.\nTherefore, whenever the psome function is called inside a loop the object will\nbe printed only a limited number of times. This can useful for debugging\ncode in particular when the data structure we want to scan is quite big and we\nwant to print only the first elements of it.