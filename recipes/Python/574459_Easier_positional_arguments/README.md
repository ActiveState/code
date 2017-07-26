## Easier positional arguments for optparse  
Originally published: 2008-07-14 00:05:27  
Last updated: 2012-02-27 12:32:11  
Author: Shekhar Tiwatne  
  
Many times I find myself write a cli that takes two/more positional arguments.\nSomething like\n  mycp file1 file2 [options]\nI have to write extra code everytime to show correct usage/hints to user if he invokes command this way\n mycp file1\nPositional arguments are required ones unlike optional arguments.\n\nThe solution below lets cli writer add a positional argument so parser can generate usage friendlier to positional args.\n\nSome inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/573441