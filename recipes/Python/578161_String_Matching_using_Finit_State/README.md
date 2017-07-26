## String Matching using a Finit State Machine  
Originally published: 2012-06-07 06:03:52  
Last updated: 2012-06-07 06:03:52  
Author: Filippo Squillace  
  
This module executes the string matching between an input sequence T and a
pattern P using a Finite State Machine.
The complexity for building the transition function is O(m^3 x |A|) where A is the
alphabet. Since the string matching function scan the input sequence only once,
the total complexity is O(n + m^3 x |A|)