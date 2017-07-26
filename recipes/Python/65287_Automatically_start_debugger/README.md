## Automatically start the debugger on an exception 
Originally published: 2001-06-22 02:47:43 
Last updated: 2001-07-13 08:39:47 
Author: Thomas Heller 
 
When Python runs a script and an uncatched exception is raised, a traceback is printed and the script is terminated.\nPython2.1 has introduced sys.excepthook, which can be used to override the handling of uncaught exceptions. This allows to automatically start the debugger on an unexpected exception, even if python is not running in interactive mode.