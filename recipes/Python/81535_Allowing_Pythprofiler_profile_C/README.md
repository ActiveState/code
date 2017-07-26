## Allowing the Python profiler to profile C modules 
Originally published: 2001-10-13 07:39:30 
Last updated: 2001-10-14 09:01:29 
Author: Richie Hindle 
 
This recipe lets you take into account time spent in C modules when profiling your Python code.  Normally the profiler only profiles Python code, so finding out how much time is spent accessing a database, running encryption code, sleeping and so on is difficult.  Profilewrap makes it easy to profile C code as well as Python code, giving you a clearer picture of where your application is spending its time.\n\nProfilewrap demonstrates how to create proxy objects at runtime that intercept calls between pre-existing pieces of code.  It also demonstrates the use of the 'new' module to create new functions on the fly.\n