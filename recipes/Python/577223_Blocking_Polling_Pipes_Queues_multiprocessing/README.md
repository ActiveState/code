## Blocking, Polling, Pipes, Queues in multiprocessing and how they are affected by the OS's time-slicing schedule

Originally published: 2010-05-08 18:18:00
Last updated: 2010-05-08 18:18:01
Author: Kaushik Ghose

This short code demonstrates how blocking calls to a Queue, while consuming less CPU, are limited in their response time by the minimum time slice the OS is willing to allocate (typically 10ms for Mac OS X and Linux). Non-blocking calls to Pipe, using poll() to check if there is data, on the other hand, give us millisecond or less response times, though they consume more CPU. In this respect doing a blocking call to a CPU is no different than adding sleep(.01) statements to a polling loop. In a way, if you execute a sleep(.01) only when you have no events in your poll you will be more efficient than if you had a blocking call pull events off your Queue one by one - because each call to Queue.get() consumes a time-slice, whereas the sleep(.01) only occurs once. 