## Generate equally-spaced floats

Originally published: 2011-09-24 18:13:12
Last updated: 2011-09-24 18:49:39
Author: Steven D'Aprano

Generating a list of equally-spaced floats can surprising due to floating point rounding. See, for example, the recipe for a [floating point range](http://code.activestate.com/recipes/577068). One way of avoiding some surprises is by changing the API: instead of specifying a start, stop and step values, instead use a start, stop and count:\n\n    >>> list(spread(0.0, 2.1, 7))\n    [0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8]\n\nLike [frange](http://code.activestate.com/recipes/577068) `spread` takes an optional mode argument to select whether the start and end values are included. By default, start is included and end is not, and exactly count values are returned.