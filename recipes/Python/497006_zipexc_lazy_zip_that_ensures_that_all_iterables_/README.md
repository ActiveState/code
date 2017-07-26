## zip_exc(), a lazy zip() that ensures that all iterables have the same length  
Originally published: 2006-08-31 03:12:12  
Last updated: 2006-08-31 03:12:12  
Author: Peter Otten  
  
Using zip(names, values) may inadvertently eat some of your data when there are, e. g., fewer values than names. This is easy to fix with assert len(names) == len(values) if the arguments' length is known, but not if they are arbitrary iterables. With zip_exc() no such glitches go unnoticed as list(zip_exc(names, values)) throws a LengthMismatch exception if the number of names and values differ.