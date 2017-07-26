## How to disablе debug logging in release version  
Originally published: 2006-07-07 05:38:09  
Last updated: 2006-07-12 08:34:36  
Author: Denis Barmenkov  
  
When you release your program to client, its a good idea to disable all the debug messages.\nIt is possible via custom configuring debug levels at all modules, but may be implemented using simple wrapper around logging.getLogger() function.