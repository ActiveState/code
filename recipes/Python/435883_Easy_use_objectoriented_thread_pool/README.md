## Easy to use object-oriented thread pool framework  
Originally published: 2005-07-02 21:03:07  
Last updated: 2005-07-19 00:51:12  
Author: Chris Arndt  
  
A thread pool is a class that maintains a pool of worker threads to perform
time consuming operations in parallel. It assigns jobs to the threads
by putting them in a work request queue, where they are picked up by the
next available thread. This then performs the requested operation in the
background and puts the results in a another queue.

The thread pool class can then collect the results from all threads from
this queue as soon as they become available or after all threads have
finished their work. It's also possible, to define callbacks to handle
each result as it comes in.

Basic usage:

>>> main = TreadPool(poolsize)
>>> requests = makeRequests(some_callable, list_of_args, callback)
>>> [main.putRequests(req) for req in requests]
>>> main.wait()

See the below for a longer, annotated usage example.