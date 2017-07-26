## quick Python profiling with hotshot  
Originally published: 2009-02-20 22:29:02  
Last updated: 2009-02-20 22:35:07  
Author: Trent Mick  
  
This is a quick snippet that I use occasionally to profile some pure-Python code, using [`hotshot`](http://docs.python.org/library/hotshot.html#module-hotshot). Basically it is this:

1. Put this `@hotshotit` decorator on the function you want to profile.
2. Run your code through some representative paces. The result will be a `<functionname>.prof` in the current directory.
3. Process the `.prof` file and print the top 20 hotspots with the given "show_stats.py" script.

Props to [Todd](http://blogs.activestate.com/toddw/) for slapping this code together.

Hotshot [is a little out of favour](http://docs.python.org/library/profile.html) now, so I should -- or Todd :) -- should really come up with an equivalent that uses `cProfile`.