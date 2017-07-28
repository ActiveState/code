## Size of Python objects (revised).  
Originally published: 2008-02-20 12:12:20  
Last updated: 2017-07-22 15:52:01  
Author: Jean Brouwers  
  
This recipe determines the size of Python objects in bytes and has been further enhanced to handle ints, namedtuples, arrays and NumPy types better.  Functions *alen* and *itemsize* have been updated.  Support for Python 2.5 and earlier and the tests/examples have been removed.  See project [Pympler](https://github.com/pympler/pympler) for unit tests.

See also other, simpler recipes like this  [Compute memory footprint of an object and its contents](http://code.activestate.com/recipes/577504).