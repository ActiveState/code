## Equally-spaced numbers (linspace)  
Originally published: 2015-01-12 22:16:31  
Last updated: 2015-01-12 22:16:37  
Author: Andrew Barnert  
  
An equivalent of [`numpy.linspace`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html), but as a pure-Python lazy sequence.

Like NumPy's `linspace`, but unlike the [`spread`](http://code.activestate.com/recipes/577068/) and [`frange`](http://code.activestate.com/recipes/577068/) recipes listed here, the `num` argument specifies the number of values, not the number of intervals, and the range is closed, not half-open.

Although this is primarily designed for floats, it will work for `Fraction`, `Decimal`, NumPy arrays (although this would be silly) and even `datetime` values.

This recipe can also serve as an example for creating lazy sequences.

See the discussion below for caveats.