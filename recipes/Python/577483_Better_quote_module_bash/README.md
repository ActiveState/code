## Better quote module for bash shells  
Originally published: 2010-12-03 09:15:48  
Last updated: 2010-12-03 09:16:45  
Author: Kevin L. Sitze  
  
This Python module quotes a Python string so that it will be treated as a single argument to commands ran via os.system() (assuming bash is the underlying shell).  In other words, this module makes arbitrary strings "command line safe" (for bash command lines anyway, YMMV if you're using Windows or one of the (less fine) posix shells).