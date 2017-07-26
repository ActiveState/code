## simplest useful (I hope!) thread pool example 
Originally published: 2004-08-31 07:43:53 
Last updated: 2004-09-08 13:53:48 
Author: John Nielsen 
 
You can find examples on how to do threading, but they do not show off a thread pool. My goal was to get as small and simple as possible working thread pool example to show off the basic ideas without having extraneous things to understand.  To show off the thread pool, I want stopping and starting of the threads to be explicit. This means the pool won't start until you are ready and will run forever until you are ready for it to stop. The main thread puts into the input queue and removes data from the output queue. The thread pool simply does the converse. Errors are also managed with another queue, so there is a clean distinction between errors and successful results.