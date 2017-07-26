## map_longest and map_strict  
Originally published: 2011-05-06 09:29:52  
Last updated: 2011-05-06 17:35:17  
Author: Steven D'Aprano  
  
In Python 3, the map builtin silently drops any excess items in its input:

    >>> a = [1, 2, 3]
    >>> b = [2, 3, 4]
    >>> c = [3, 4, 5, 6, 7]
    >>> list(map(lambda x,y,z: x*y+z, a, b, c))
    [5, 10, 17]

In Python 2, map pads the shorter items with None, while itertools.imap drops the excess items. Inspired by this, and by itertools.zip_longest, I have map_longest that takes a value to fill missing items with, and map_strict that raises an exception if a value is missing.

    >>> list(map_longest(lambda x,y,z: x*y+z, a, b, c, fillvalue=0))
    [5, 10, 17, 6, 7]
    >>> list(map_strict(lambda x,y,z: x*y+z, a, b, c))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 9, in map_strict
    ValueError: too few items in iterable