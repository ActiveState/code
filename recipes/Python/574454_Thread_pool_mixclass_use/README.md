## Thread pool mixin class for use with SocketServer.TCPServer 
Originally published: 2008-07-10 11:50:11 
Last updated: 2008-07-10 18:52:58 
Author: Michael Palmer 
 
This is intended as a drop-in replacement for the ThreadingMixIn class in module SocketServer of the standard lib. Instead of spawning a new thread for each request, requests are processed by of pool of reusable threads.