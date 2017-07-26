## Thread-safe MultiQueue  
Originally published: 2005-02-03 06:15:31  
Last updated: 2005-02-05 17:13:00  
Author: Dominic Fox  
  
A class that contains a dictionary of named queues, with read requests blocking until a message has been added to any one of a supplied list of queues.