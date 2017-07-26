## Profile decoratorOriginally published: 2011-08-02 19:07:26 
Last updated: 2011-08-02 19:08:58 
Author: Giampaolo Rodolà 
 
A decorator for profiling a function which prints profiling results to stdout.\nThis was originally proposed as a patch for inclusion into python stdlib:\n\nhttp://bugs.python.org/issue9285\n\nNote that on certain Linux systems pstats module isn't available, despite it is supposed to be part of Python stdlib. On my Ubuntu box I had to run "sudo apt-get install python-profile" first.