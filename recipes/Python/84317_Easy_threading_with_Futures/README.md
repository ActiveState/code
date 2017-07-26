## Easy threading with Futures  
Originally published: 2001-10-30 10:15:20  
Last updated: 2002-04-16 21:12:21  
Author: David Perry  
  
Although Python's thread syntax is nicer than in many languages, it can still be a pain if all one wants to do is run a time-consuming function in a separate thread, while allowing the main thread to continue uninterrupted.  A Future provides a legible and intuitive way to achieve such an end.