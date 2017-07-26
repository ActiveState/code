## PyHeartbeat - detecting inactive computers 
Originally published: 2001-03-26 03:55:09 
Last updated: 2004-09-16 18:52:39 
Author: Nicola Larosa 
 
PyHeartbeat detects inactive computers by sending and receveing "heartbeats" as UDP packets on the network, and keeping track of how much time passed since each known computer sent its last heartbeat. The concurrency in the server is implemented using threads first, and then again using the Twisted Matrix framework.