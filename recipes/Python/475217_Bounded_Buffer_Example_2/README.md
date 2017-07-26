## Bounded Buffer Example (2)  
Originally published: 2006-03-29 10:11:15  
Last updated: 2006-03-29 10:11:15  
Author: Stephen Chappell  
  
This is the second example solution to the bounded
buffer problem. By looking at the code, you may
notice that it has several features that exapand
on what is demonstrated in the first example.
First of all, it accepts several new command line
arguments that allow customization of the operation
of this recipe (including an optional seed argument).
Furthermore, this recipe features a fourth thread
that takes care of printing for the producer and
consumer threads. Of all the improvements in this
example, one of the nicest involves improved
functions for the threads being executed.