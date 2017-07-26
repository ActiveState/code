## Submit multiple concurrent batch jobs, with flexible throttling and timing.  
Originally published: 2007-11-11 10:33:36  
Last updated: 2007-11-11 10:33:36  
Author: Mark Pettit  
  
Submit a series of batch commands (as expected by the os.system() function).
Each will be submitted in a separate python thread, but will be a separate process, hence will take advantage of multi-core cpu's.  A maximum number of simultaneous jobs can be set - throttling.  A maximum time can be set before the routine will return, else it waits until all are completed.