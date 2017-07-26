## Threaded Queue Minder 
Originally published: 2005-05-26 23:55:24 
Last updated: 2005-09-10 23:35:24 
Author: Jonathan Kolyer 
 
This class will run a timer that checks a Queue.Queue object at a given interval.  This is useful for monitoring messages between threads.  You give it a callback, interval, and it does the rest:  When its finds a message, your callback is fired up.