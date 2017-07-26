## Install bound methods in an instance  
Originally published: 2003-09-19 02:05:17  
Last updated: 2003-09-19 02:05:17  
Author: john mclaughlin  
  
Python has an extremely flexible object model that allows for assignment of arbitrary objects to arbitrary attributes of instances. I would like to do something like this:
def button( self ): print "Pressed!"
and then assign it to an instance:
mywidget.bigred = button
and call it:
mywidget.bigred()

However this doesn't work because the attribute needs to be a bound method, not a function. Also, the name of the installed function remains button (eg. in stack traces), when we would like it to be bigred.

This recipe provides the installmethod() and renamefunction() functions to solve this problem.