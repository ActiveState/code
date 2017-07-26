## Thread-specific storage  
Originally published: 2001-07-25 16:13:31  
Last updated: 2001-08-08 18:06:31  
Author: John E. Barham  
  
The get_thread_storage() function described below returns a thread-specific storage dictionary.  (It is a generalization of the get_transaction() function from ZODB, the object database underlying Zope.)  The returned dictionary can be used to store data that is "private" to the thread.