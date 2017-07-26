## ThreadSafeProxy  
Originally published: 2005-01-19 10:16:49  
Last updated: 2005-01-19 10:16:49  
Author: Shannon -jj Behrens  
  
This is a proxy for an instance of some class called Foo.  Any
thread can use the one proxy, and the proxy will automatically look up the
thread specific instance of Foo.  This is great if you have a global function
in someone else's code that you need to swap out for something "thread safe".