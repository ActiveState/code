## "conditionals" in expressions  
Originally published: 2001-03-26 12:15:33  
Last updated: 2001-04-08 14:57:10  
Author: Alex Martelli  
  
Python's "if" is a _statement_, and there is no conditional _operator_ (like C's "a?b:c" ternary) that we could use where expressions are needed (lambdas, etc); however, with some due care, equivalents can easily be coded.