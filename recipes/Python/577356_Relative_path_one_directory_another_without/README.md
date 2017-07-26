## Relative path from one directory to another without explicit string functions (unix only) 
Originally published: 2010-08-13 05:20:15 
Last updated: 2011-04-11 13:02:32 
Author: Denis Barmenkov 
 
I saw a recipe 208993 messed up with os.sep and '../' and decide to write near-pure-Python version.\nos.sep used in string expressions only for testing for root directory.\n\nFunction deal with Unix paths (root: "/"), Windows systems are not supported (root: "C:\\").