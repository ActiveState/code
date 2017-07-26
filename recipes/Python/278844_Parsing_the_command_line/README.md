## Parsing the command line

Originally published: 2004-04-18 00:37:24
Last updated: 2004-04-18 08:15:21
Author: Michele Simionato

The module optparse was a great addition to Python 2.3, since it is much more\npowerful and easier to use than getopt. Using optparse, writing command-line\ntools is a breeze. However, the power of optparse comes together with a certain\nverbosity. This recipe allows to use optparse with a minimum of boilerplate,\ntrading flexibility for easy of use. Still, it covers 95% of my common needs,\nso I think it may be useful to others.