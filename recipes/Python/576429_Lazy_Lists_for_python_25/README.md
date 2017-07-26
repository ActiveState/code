## Lazy Lists for python 2.5

Originally published: 2008-08-18 19:59:03
Last updated: 2008-08-18 19:59:03
Author: Michael Pust

Dan Spitz submitted a recipe ( [576410](http://code.activestate.com/recipes/576410/) ) for recursively defined lazy lists backed by a generator.  Only catch was that it was written for python 3k.  But there is nothing intrinsic in 3k that prevents you from having the same functionality in python 2.5, so I am supplying the backport here.