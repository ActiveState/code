## String Matching using a Finit State MachineOriginally published: 2012-06-07 06:03:52 
Last updated: 2012-06-07 06:03:52 
Author: Filippo Squillace 
 
This module executes the string matching between an input sequence T and a\npattern P using a Finite State Machine.\nThe complexity for building the transition function is O(m^3 x |A|) where A is the\nalphabet. Since the string matching function scan the input sequence only once,\nthe total complexity is O(n + m^3 x |A|)