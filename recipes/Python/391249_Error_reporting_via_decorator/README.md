## Error reporting via decorator  
Originally published: 2005-03-10 16:13:58  
Last updated: 2005-03-10 16:13:58  
Author: Scott David Daniels  
  
A Python 2.4 (or later) decorator can be used to watch for unhandled exceptions,\neven in hybrid environments like wxPython.  You place the decorator around methods that will be invoked by the wxWidgets code.  The only big trick is a dance that may be necessary to provide access to values only available after the wxPthon app is started.