## Wrap a a file-like object in another that calls a user callback whenever read() is called on it. 
Originally published: 2013-09-25 01:49:53 
Last updated: 2013-09-25 01:54:53 
Author: Martin Miller 
 
Wraps a file-like object in another, but also calls a user callback with the number of bytes read whenever its `read()` method is called. Used for tracking upload progress, for example for a progress bar in a UI application.\n