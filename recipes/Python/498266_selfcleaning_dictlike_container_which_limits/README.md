## A self-cleaning dict-like container which limits the number and lifetime of its items  
Originally published: 2006-11-15 15:16:55  
Last updated: 2006-11-15 23:51:50  
Author: Michael Palmer  
  
This container stores its items both in a dict (for direct access) and in a bi-directionally linked list, which enables it to update itself in essentially O(1) time. No iteration over the entire list is ever needed, no separate thread is required for cleaning either. Should be useful e.g. for session storage in web servers.