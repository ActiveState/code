## Page through iterable N items at a time  
Originally published: 2008-02-19 04:39:10  
Last updated: 2008-02-20 18:57:43  
Author: Wade Leftwich  
  
Simple generator accepts an iterable L and an integer N and yields a series of sub-generators, each of which will in turn yield N items from L.