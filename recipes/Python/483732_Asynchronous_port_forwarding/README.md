## Asynchronous port forwardingOriginally published: 2006-04-06 12:20:53 
Last updated: 2006-04-06 19:25:57 
Author: Nicolas Lehuen 
 
This forward the TCP traffic from your machine to another host, and back in the the other way. It uses asynchronous socket thanks to ye olde asyncore module, which was used by Zope up until recently (they integrated the Twisted reactor). As a consequence, it should be able to handle a great number of connections without crumbling under the weight of many threads.