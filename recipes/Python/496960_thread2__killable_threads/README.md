## thread2 -- killable threads  
Originally published: 2006-08-11 03:01:10  
Last updated: 2012-08-09 20:14:33  
Author: tomer filiba  
  
A little module that extends the threading's module functionality -- allows one thread to raise exceptions in the context of another thread. By raising SystemExit, you can finally kill python threads :)