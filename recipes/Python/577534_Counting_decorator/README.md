###Counting decorator

Originally published: 2011-01-07 11:22:55
Last updated: 2011-01-07 11:22:55
Author: Noufal Ibrahim

To be used as a decorator for a function that will maintain the number of times it was called. \nHere is an example use. \n\n    >>> def test():\n    ...    print "Hello"\n    ... \n    >>> test = counter(test)\n    >>> test()\n    Hello\n    >>> test()\n    Hello\n    >>> test()\n    Hello\n    >>> test()\n    Hello\n    >>> test()\n    Hello\n    >>> test.invocations\n    5\n    >>> test()\n    Hello\n    >>> test.invocations\n    6\n    >>> \n