## Equally-spaced floats part 2

Originally published: 2011-09-27 15:47:59
Last updated: 2011-09-27 15:48:00
Author: Steven D'Aprano

See the recipe [here](http://code.activestate.com/recipes/577878) for a description of the problem.\n\nThis variant allows the user to choose between two APIs, either by supplying the count, start value and end value:\n\n    >>> list(spread(5, 1.0, end=2.0))\n    [1.0, 1.2, 1.4, 1.6, 1.8]\n\nor the count, start value and step size:\n\n    >>> list(spread(5, 1.0, step=-0.25))\n    [1.0, 0.75, 0.5, 0.25, 0.0]\n\nAs before, the count argument specifies how many subdivisions are made. The optional argument `mode` selects whether the start and end values are included. By default, start is included and end is not, and exactly count values are returned.