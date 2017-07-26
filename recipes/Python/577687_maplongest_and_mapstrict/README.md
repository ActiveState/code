## map_longest and map_strict

Originally published: 2011-05-06 09:29:52
Last updated: 2011-05-06 17:35:17
Author: Steven D'Aprano

In Python 3, the map builtin silently drops any excess items in its input:\n\n    >>> a = [1, 2, 3]\n    >>> b = [2, 3, 4]\n    >>> c = [3, 4, 5, 6, 7]\n    >>> list(map(lambda x,y,z: x*y+z, a, b, c))\n    [5, 10, 17]\n\nIn Python 2, map pads the shorter items with None, while itertools.imap drops the excess items. Inspired by this, and by itertools.zip_longest, I have map_longest that takes a value to fill missing items with, and map_strict that raises an exception if a value is missing.\n\n    >>> list(map_longest(lambda x,y,z: x*y+z, a, b, c, fillvalue=0))\n    [5, 10, 17, 6, 7]\n    >>> list(map_strict(lambda x,y,z: x*y+z, a, b, c))\n    Traceback (most recent call last):\n      File "<stdin>", line 1, in <module>\n      File "<stdin>", line 9, in map_strict\n    ValueError: too few items in iterable