## Timeout function using threading 
Originally published: 2006-02-09 14:30:29 
Last updated: 2006-02-09 14:30:29 
Author: dustin lee 
 
Using signals to timeout a function such as in:\nhttp://www.pycs.net/users/0000231/weblog/2004/10/\nhttp://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/307871\nwon't work if the function you are calling overrides the alarm.  Using threads gives you away around this.