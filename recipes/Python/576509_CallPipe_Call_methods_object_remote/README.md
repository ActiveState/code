## CallPipe: Call the methods of an object in a remote processOriginally published: 2008-09-17 17:21:16 
Last updated: 2008-09-17 17:33:36 
Author: david decotigny 
 
I am process A and I own object Obj. Now I decide to fork(): process B is born.\n\nHow do I do to make process B call the methods of A's object Obj (and not the methods of its own copy of Obj...) ?\n\nThis is what this module does: you create the "CallPipe" for Obj prior to fork()ing, and then process B can call any method of A's object Obj through it.