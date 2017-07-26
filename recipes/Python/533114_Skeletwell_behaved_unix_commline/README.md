## Skeleton for well behaved unix command line toolsOriginally published: 2007-09-27 05:00:28 
Last updated: 2007-09-27 05:00:28 
Author: Alfred Schilken 
 
This skeleton is a good start for well behaved unix command line tools.\nThe module optparse is used to get arguments and options and to print usage and help.\nLike typical unix tools with one or two file arguments\nit handles stdin and stdout if not enough arguments are given.