## Get UNIX domain socket peer credentials (FreeBSD)  
Originally published: 2008-06-06 05:46:59  
Last updated: 2008-06-06 05:46:59  
Author: Kris Kennaway  
  
Return a nested tuple of (uid, (gids)) for a UNIX domain socket, on FreeBSD.  This is useful for access control on local servers, which can limit access based on the ID of the connecting user.