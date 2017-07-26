## Generate HTML syntax-highlighted listings for any file using pygments  
Originally published: 2009-06-16 10:37:44  
Last updated: 2011-02-01 14:21:59  
Author: ccpizza   
  
Generates HTML highlighted code listings for source code files in any language known to \npygments. For a list of supported formats see http://pygments.org/languages\n\nMake sure you have [pygments](http://pygments.org) is installed. Try `easy_install pygments`.\n\nExample usage:\n\n*output to stdout:*\n\n    python highlight.py my_source_file.java  \n\n*output to file:*\n\n    python highlight.py my_source_file.java > my_source_file.html