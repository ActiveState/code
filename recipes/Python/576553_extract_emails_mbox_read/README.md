## extract emails from a mbox read on stdin 
Originally published: 2008-11-03 10:39:14 
Last updated: 2013-09-07 10:24:17 
Author: Romain Dartigues 
 
The Python `mailbox.mbox` class require a real file to initialize, which was an issue in my case. These simple functions let you iter through a mailbox read from a read-only file descriptor (like `sys.stdin`).\n\nThis script use the generators which were introduced in Python-2.2. Let me know if you are interested a similar functionnality on older Python versions.