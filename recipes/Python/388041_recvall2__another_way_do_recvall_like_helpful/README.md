## recvall2  (another way to do a recvall like the helpful sendall)  
Originally published: 2005-02-18 15:25:09  
Last updated: 2005-02-18 15:25:09  
Author: John Nielsen  
  
Socket.sendall is very handy for sending. It would be nice if there was a socket.recvall.
Unfortunatelty, receiving data is hard. One way to to do a recvall, is to use timeouts that get reset if any amount of data arrives.  Useful, if you know almost nothing about what you are receiving.

http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/213239

Another, if you can control the sender, is to use a sentinal or marker, and  send when the end has arrived.

This example, shows  a really simple way, to do that.  The assumption is that you have a unique enough string as an end marker. You pass a socket to either of these functions. The sender takes on the end marker and the receiver looks for it.