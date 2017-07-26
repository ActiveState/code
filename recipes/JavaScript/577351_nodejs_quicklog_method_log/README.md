## node.js quicklog method to log to a file  
Originally published: 2010-08-11 05:08:57  
Last updated: 2010-08-11 05:08:57  
Author: Trent Mick  
  
I tend to have a "quicklog" method for a few of the languages I'm working in to do logging when stdout/stderr isn't necessarily available (GUI app) or convenient (lots of other output on stdout, etc.). My usage with [nodejs](http://nodejs.org) was while working on the node REPL. Log output to stdout interfered with the REPL.