## Twisted / BitTorrent ::  Client / Server  
Originally published: 2005-09-13 22:05:20  
Last updated: 2005-10-30 01:24:39  
Author: Jonathan Kolyer  
  
Two modules that run a BitTorrent server, and uses Twisted as a client to coordinate control-message passing, and progress monitoring.  The server can be run as a separate process, or as a thread within the client -- the same messages can be passed back and forth.\n\nControl messages can cancel individual downloads (or the whole process), as well as pause downloading.  Progress queries can be invoked through the client, which will ping the server, and report back each downloads' progress.