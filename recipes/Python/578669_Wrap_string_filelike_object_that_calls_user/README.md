## Wrap a string in a file-like object that calls a user callback whenever read() is called on the stream  
Originally published: 2013-09-22 21:48:02  
Last updated: 2013-09-22 21:48:03  
Author: Ben Hoyt  
  
Wraps a string in a read-only file-like object, but also calls a user callback with the number of bytes read whenever `read()` is called on the stream. Used for tracking upload progress, for example for a progress bar in a UI application.