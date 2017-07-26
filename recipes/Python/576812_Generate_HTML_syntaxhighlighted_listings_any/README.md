## Generate HTML syntax-highlighted listings for any file using pygments  
Originally published: 2009-06-16 10:37:44  
Last updated: 2011-02-01 14:21:59  
Author: ccpizza   
  
Generates HTML highlighted code listings for source code files in any language known to 
pygments. For a list of supported formats see http://pygments.org/languages

Make sure you have [pygments](http://pygments.org) is installed. Try `easy_install pygments`.

Example usage:

*output to stdout:*

    python highlight.py my_source_file.java  

*output to file:*

    python highlight.py my_source_file.java > my_source_file.html