## Managing thread lifetime 
Originally published: 2001-10-17 13:40:15 
Last updated: 2001-10-18 21:12:51 
Author: Michael Robin 
 
If you're familiar with thread programming, Python is reasonably straightforward to work with, once you realize the global interpreter lock is around; however, sometimes they can be trouble. One case is when threads don't die when you expect them to. Resorting to infrequent polling, even if more advanced logic is active in your program, is one way to deal with this, especially during debugging.