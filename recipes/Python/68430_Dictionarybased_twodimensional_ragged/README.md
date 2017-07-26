## A Dictionary-based two-dimensional ragged array.  
Originally published: 2001-09-23 09:31:13  
Last updated: 2001-10-03 04:40:03  
Author: Peter Olsen  
  
This class implements a two-dimensional ragged array using nested dictionaries.

As written this class requires Python 2.2 or later.  This meets my requirements, but it may not
meet yours.

Klaus Alexander Seistrup has described a way to get around this restriction by substituting
"UserDict.UserDict" for "dictionary" as the base class.  I believe this solves the problem
for Python versions at least as far back as 1.5.2.  This approach will require some editing of
the insertion and retrieval functions to make it work.

Thanks Klaus!