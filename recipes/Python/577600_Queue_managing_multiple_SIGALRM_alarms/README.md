## Queue for managing multiple SIGALRM alarms concurrentlyOriginally published: 2011-03-07 18:14:08 
Last updated: 2012-12-06 18:58:11 
Author: Glenn Eychaner 
 
In asynchronous code, *signal.alarm()* is extremely useful for setting and handling timeouts and other timed and periodic tasks. It has a major limitation, however, that only one alarm function and alarm time can be set at a time; setting a new alarm disables the previous alarm. This package uses a *heapq* to maintain a queue of alarm events, allowing multiple alarm functions and alarm times to be set concurrently.