## An interval mapping data structureOriginally published: 2010-12-23 12:51:26 
Last updated: 2010-12-23 12:51:27 
Author: Matteo Dell'Amico 
 
This structure is a kind of dictionary which allows you to map data intervals to values. You can then query the structure for a given point, and it returns the value associated to the interval which contains the point. Boundary values don't need to be an integer.\n\nIn this version, the excellent [blist](http://pypi.python.org/pypi/blist/) library by Daniel Stutzbach is used for efficiency. By using the collections.MutableMapping abstract base class, the whole signature of mappings is supported.