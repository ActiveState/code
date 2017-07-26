## asyncore scheduler  
Originally published: 2011-07-25 21:17:07  
Last updated: 2011-07-25 23:42:21  
Author: Giampaolo Rodolà  
  
The thing I miss mostly in asyncore is a system for calling a function after a certain amount of time without blocking. This is crucial for simple tasks such as disconnecting a peer after a certain time of inactivity or more advanced use cases such as [bandwidth throttling](http://code.google.com/p/pyftpdlib/source/browse/tags/release-0.6.0/pyftpdlib/ftpserver.py#1048).

This recipe was initially inspired by Twisted's internet.base.DelayedCall class:

http://twistedmatrix.com/trac/browser/tags/last_vfs_and_web2/twisted/internet/base.py#L34
 
...then included into pyftpdlib:

http://code.google.com/p/pyftpdlib/issues/detail?id=72
 
...and finally proposed for inclusion into asyncore:

http://bugs.python.org/issue1641