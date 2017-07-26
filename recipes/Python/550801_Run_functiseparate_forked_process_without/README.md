## Run a function in a separate (forked) process without blockingOriginally published: 2008-02-27 13:36:13 
Last updated: 2008-02-28 22:22:18 
Author: Gary Eakins 
 
A procedure that runs a function asynchronously in a forked process (Availability: Macintosh, Unix). The return from the specified function is written into an anonymous memory map (mmap: requires +Python 2.5).  This can be useful for releasing resources used by the function such as memory, updating a gui or cli widget, or other weirdness.