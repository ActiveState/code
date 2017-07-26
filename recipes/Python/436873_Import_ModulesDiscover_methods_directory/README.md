## Import Modules/Discover methods from a directory name  
Originally published: 2005-07-14 08:55:00  
Last updated: 2005-07-15 13:15:48  
Author: Jesse Noller  
  
For something I am working on, I needed the ability to scan a supplied directory, adding the directory to the sys.path within Python, and then blanket import the modules within that directory. Following that, I had to filter any builtin or special methods within those modules and return a list of the methods for the module I had imported.

The script is very simplistic in what it does.