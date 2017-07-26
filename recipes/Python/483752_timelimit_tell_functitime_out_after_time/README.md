###timelimit: tell a function to time out after a time limit

Originally published: 2006-04-10 18:39:47
Last updated: 2006-04-10 18:39:47
Author: Aaron Swartz

Have a function that you want to put a time limit on? Just use this decorator like so:\n\n@timelimit(10)\ndef myfunction(...): ...\n\nwill limit myfunction to 10 seconds, raising TimeoutError if it takes longer.