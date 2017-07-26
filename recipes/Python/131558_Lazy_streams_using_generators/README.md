## Lazy streams using generators 
Originally published: 2002-06-05 11:23:00 
Last updated: 2002-06-05 11:23:00 
Author: Ben Wolfson 
 
This class allows you to use generators as more list-like streams.  The chief advantage is that it is impossible to iterate through a generator more than once, while a stream can be re-used like a list.