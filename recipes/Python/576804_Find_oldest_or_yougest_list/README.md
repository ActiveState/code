## Find the oldest (or yougest) of a list of files  
Originally published: 2009-06-10 16:08:13  
Last updated: 2009-06-10 16:08:13  
Author: Micah Elliott  
  
Sometimes you need to perform an operation on the oldest of a set of files.  Using *get_oldest_file* you could implement an age-based priority queue that processes files from oldest to newest.  The list of files you pass in may be from a *glob* of a single directory or some more elaborate search routine.