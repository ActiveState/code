## Simple shelve with Linux file locking 
Originally published: 2008-12-21 05:50:07 
Last updated: 2008-12-21 05:50:07 
Author: Michael Ihde 
 
The shelve module is a easy way to add persistence to your application via a DBM database.  However, if you have multiple reader/writer combination you need to lock the file to prevent corruption.  The shelve module itself does not provide locking because it is platform specific.  If you only need Linux, this simple module provide an easy way to support locking using dynamically added methods.