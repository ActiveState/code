## Install bound methods in an instance  
Originally published: 2003-09-19 02:05:17  
Last updated: 2003-09-19 02:05:17  
Author: john mclaughlin  
  
Python has an extremely flexible object model that allows for assignment of arbitrary objects to arbitrary attributes of instances. I would like to do something like this:\ndef button( self ): print "Pressed!"\nand then assign it to an instance:\nmywidget.bigred = button\nand call it:\nmywidget.bigred()\n\nHowever this doesn't work because the attribute needs to be a bound method, not a function. Also, the name of the installed function remains button (eg. in stack traces), when we would like it to be bigred.\n\nThis recipe provides the installmethod() and renamefunction() functions to solve this problem.