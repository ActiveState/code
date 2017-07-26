###And yet another round-robin generator

Originally published: 2013-11-13 19:30:28
Last updated: 2013-11-13 19:30:29
Author: Jan Müller

I know that there is a [nice recipe](http://code.activestate.com/recipes/528936-roundrobin-generator/) already that even made it into the [Python documentation](http://docs.python.org/2/library/itertools.html), but this one is more concise and at the same time simpler.\n\n    >>> list(roundrobin('ABC', 'D', 'EF'))\n    ['A', 'D', 'E', 'B', 'F', 'C']\n