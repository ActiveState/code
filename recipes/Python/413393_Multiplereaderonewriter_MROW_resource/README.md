## Multiple-reader-one-writer (MROW) resource lockingOriginally published: 2005-05-05 20:12:59 
Last updated: 2005-05-07 04:23:52 
Author: Matthew Scott 
 
In multithreaded apps, there is at times the need to control access to a resource to ensure data consistency and integrity. Multiple-reader, one-writer locking allows efficient read access by multiple threads, while ensuring that a write does not overlap any reads nor another write.