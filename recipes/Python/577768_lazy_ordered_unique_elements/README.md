## lazy ordered unique elements from an iteratorOriginally published: 2011-06-23 09:40:50 
Last updated: 2011-06-23 16:36:38 
Author: Andrew Dalke 
 
This implements a "unique" filter. Its input is an iterator of hashable items. It returns an iterator containing only the unique items of the input, in input order. That is, list(unique("cabbage")) produces ["c", "a", "b", "g"]. The implementation is lazy. The function supports the "key" parameter, which provides an alternate form of comparison.\n\n(Note: a better version of this is available from the itertools documentation as unique_everseen )