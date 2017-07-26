## logging support for python daemon 
Originally published: 2010-10-25 15:22:17 
Last updated: 2010-10-25 15:22:18 
Author: Bud P. Bruegger 
 
The recipe shows how to subclass python-daemon's [1] DaemonContext to add logging support.  In particular, it is possible to ask to keep the files related to a list of loggers (loggers_preserve) open and to redirect stdout and stderr to a logger (e.g., one using a RotatingFileHandler).  \n\n[1] See http://pypi.python.org/pypi/python-daemon/