## Safe unicode representationOriginally published: 2011-03-17 23:28:39 
Last updated: 2011-03-17 23:28:40 
Author: Sridhar Ratnakumar 
 
Safely convert any given string type (text or binary) to unicode. You won't get UnicodeDecodeError error, at the cost of ignoring those errors during conversion, which is useful for debugging and logging. This recipe requires the [six](http://code.activestate.com/pypm/six/) package.