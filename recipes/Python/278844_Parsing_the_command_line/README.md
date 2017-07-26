## Parsing the command line  
Originally published: 2004-04-18 00:37:24  
Last updated: 2004-04-18 08:15:21  
Author: Michele Simionato  
  
The module optparse was a great addition to Python 2.3, since it is much more
powerful and easier to use than getopt. Using optparse, writing command-line
tools is a breeze. However, the power of optparse comes together with a certain
verbosity. This recipe allows to use optparse with a minimum of boilerplate,
trading flexibility for easy of use. Still, it covers 95% of my common needs,
so I think it may be useful to others.