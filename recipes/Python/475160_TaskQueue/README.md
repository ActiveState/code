## TaskQueue

Originally published: 2006-03-21 01:50:12
Last updated: 2006-03-25 13:00:38
Author: Raymond Hettinger

Queue subclass to simplify working with consumer threads.  Keeps a count of tasks put into the queue and lets the consumer thread report when each task has been retrieved AND PROCESSED COMPLETELY.  This reporting supports a join() method that blocks untils all submitted tasks have been fully processed.