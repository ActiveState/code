## Persistent, lazy, caching, dictionaryOriginally published: 2006-04-28 21:27:26 
Last updated: 2006-04-28 21:27:26 
Author: Alec Thomas 
 
A persistent, lazy, caching, dictionary, using the anydbm module for persistence. Keys must be basic strings (this is an anydbm limitation) and values must be pickle-able objects.