## Decorator to expose local variables of a function after executionOriginally published: 2010-07-07 00:55:05 
Last updated: 2010-07-07 22:01:23 
Author: Pietro Berkes 
 
Decorator to expose the local variables defined in the inner scope of a function. At the exit of the decorated function (regular exit or exceptions), the local dictionary is copied to a read-only property, `locals`.\n\nThe main implementation is based on injecting bytecode into the original function, and requires the lightweight module `byteplay` (available [here](http://code.google.com/p/byteplay/)). See below for an alternative implementation that only uses the standard library.\n