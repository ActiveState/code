## Parallel loop on index and sequence-item  
Originally published: 2001-03-15 07:20:10  
Last updated: 2001-07-04 08:05:36  
Author: Alex Martelli  
  
zip() stops zipping at the shortest of its sequence-arguments and thus also allows unbounded-sequence arguments.  This affords, for example, a very spare idiom for the frequent need of a parallel loop on index and sequence-item.