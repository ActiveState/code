## Active Objects  
Originally published: 2005-02-01 03:08:38  
Last updated: 2005-02-03 20:09:13  
Author: Dominic Fox  
  
Based on the recipe for active objects given in "Concepts, Techniques, and Models of Computer Programming", by Peter van Roy and Seif Haridi, the ActiveObject class wraps an instance of a passive object and forwards messages to this object via a thread-safe message queue. The passive object processes the messages on its own thread, and returns the results to the caller via an AsynchResult object that can be used to block whilst waiting for a result, or to register callbacks to be called when a result is available.