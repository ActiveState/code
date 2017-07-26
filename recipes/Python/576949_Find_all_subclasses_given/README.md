## Find all subclasses of a given class

Originally published: 2009-11-04 20:00:22
Last updated: 2009-11-04 20:26:08
Author: Gabriel Genellina

itersubclasses(cls) returns a generator over all subclasses of cls, in depth first order.  cls must be a new-style class; old-style classes are *not* supported.