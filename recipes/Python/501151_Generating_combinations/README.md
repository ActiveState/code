## Generating combinations in blocks  
Originally published: 2007-01-23 23:44:31  
Last updated: 2007-01-26 02:30:08  
Author: George Sakkis  
  
This recipe is yet another combination generator, with an extra twist: the generated combinations can be yielded in blocks of a given size. This comes useful (or necessary) when processing arbitrarily long or infinite iterables in bounded-size blocks.