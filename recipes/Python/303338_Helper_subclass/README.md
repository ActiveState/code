## Helper subclass for win32pdhquery  
Originally published: 2004-09-03 10:03:51  
Last updated: 2004-09-03 10:03:51  
Author: Brett Cannon  
  
One of the few perks one can have when developing on Windows (at least NT or newer) is the use of the Performance Data Helper (the PDH can be found on Windows XP under the Control Panel at Administrative Tools -> Performance) for system statistics gathering.  There is a bevy of counters available that can greatly help you measure the impact your code has on the current system.\n\nAnd luckily win32all provides a wrapper to create counters.  The only drawback, though, is that the API is not the best in the world.  So, to help deal with that I wrote a subclass to help with adding counters and formatting the output in a more usable fashion as either CSV or a dict that can be pickled.