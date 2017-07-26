## lazy property

Originally published: 2009-04-15 14:33:31
Last updated: 2009-04-26 18:10:55
Author: Sridhar Ratnakumar

Python does not have lazy evaluation syntax features built-in, but fortunately decorators can be used with new-style classes to emulate such a feature. There are cases where one wants ``foo.property`` to return the actual property whose calculation takes significant amount of time.\n\nThis recipe adapts the existing `property` to provide a `lazypropery` decorator that does this.\n\nSee the first comment below for an example usage.\n\nAlso see: [lazy initialization](http://en.wikipedia.org/wiki/Lazy_initialization)