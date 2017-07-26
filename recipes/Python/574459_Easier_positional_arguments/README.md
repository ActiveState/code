## Easier positional arguments for optparse  
Originally published: 2008-07-14 00:05:27  
Last updated: 2012-02-27 12:32:11  
Author: Shekhar Tiwatne  
  
Many times I find myself write a cli that takes two/more positional arguments.
Something like
  mycp file1 file2 [options]
I have to write extra code everytime to show correct usage/hints to user if he invokes command this way
 mycp file1
Positional arguments are required ones unlike optional arguments.

The solution below lets cli writer add a positional argument so parser can generate usage friendlier to positional args.

Some inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/573441