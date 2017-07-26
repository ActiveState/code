## Technique for cyclical iteration  
Originally published: 2009-11-19 14:58:00  
Last updated: 2009-12-03 23:08:38  
Author: Raymond Hettinger  
  
Solution to the Hamming Number problem.  Demonstrates a lazy evaluation evaluation technique using itertools.tee() to feed an iterator into itself.   This is a common technique with Haskell.  The deferred_output() function is the key technique for implementing a forward reference to the output of the stream.