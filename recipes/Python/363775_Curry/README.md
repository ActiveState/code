## Curry  
Originally published: 2005-01-19 10:00:40  
Last updated: 2005-01-19 18:02:22  
Author: Shannon -jj Behrens  
  
Suppose you have a function "sum(a, b)".  This class lets you\ndo things like:\n\n    plus4 = Curry(sum, 4)\n    print plus4(5)