## Generic command-line option parser

Originally published: 2005-06-10 06:16:18
Last updated: 2005-06-10 13:46:18
Author: Anand 

When writing applications that take command-line arguments in Python, one has to make a choice between the two command-line parsing modules, getopt and optparse. Optparse though more powerful than getopt is available only since Python 2.3. Hence if you are writing a program targeted at Python 2.2 +, you are mostly constrained with using getopt and writing command line parsing code on top of it.\n\nThis recipe provides a solution to this problem. It masks the actual module used for option parsing from the application. If optparse is available it is used, otherwise the parser class defaults to getopt. The application only requires to pass a dictionary of\noption keys and their settings, in a format inspired by optparse, but using tuples.