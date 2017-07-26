## Easy to use object-oriented thread pool framework 
Originally published: 2005-07-02 21:03:07 
Last updated: 2005-07-19 00:51:12 
Author: Chris Arndt 
 
A thread pool is a class that maintains a pool of worker threads to perform\ntime consuming operations in parallel. It assigns jobs to the threads\nby putting them in a work request queue, where they are picked up by the\nnext available thread. This then performs the requested operation in the\nbackground and puts the results in a another queue.\n\nThe thread pool class can then collect the results from all threads from\nthis queue as soon as they become available or after all threads have\nfinished their work. It's also possible, to define callbacks to handle\neach result as it comes in.\n\nBasic usage:\n\n>>> main = TreadPool(poolsize)\n>>> requests = makeRequests(some_callable, list_of_args, callback)\n>>> [main.putRequests(req) for req in requests]\n>>> main.wait()\n\nSee the below for a longer, annotated usage example.