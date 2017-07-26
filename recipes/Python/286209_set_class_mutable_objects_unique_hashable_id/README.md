## A set class for mutable objects with unique and hashable 'id' attributesOriginally published: 2004-07-07 18:34:01 
Last updated: 2004-07-07 18:34:01 
Author: Duncan Smith 
 
The following KeyedSet class mirrors the builtin set class as closely as possible, whilst maintaining the general flexibility of a dictionary.  The only requirement is that each set item has a distinct 'id' attribute.  The usual set operations are implemented, but items can also be referenced via their id.