## Qt + Twisted (threadedselectreactor) 
Originally published: 2006-01-17 19:37:28 
Last updated: 2006-01-17 19:37:28 
Author: Jonathan Kolyer 
 
Starting with the recipe "Network Ping Pong using Twisted Prespective Broker" (181905), this recipe integrates Qt using the threadedselectreactor.  An alternative to qtreactor, this recipe allows dispatching messages over the perspective broker while running the Qt event loop.  It basically shows how to use reactor.interleave(aFunction) within the context of Qt.