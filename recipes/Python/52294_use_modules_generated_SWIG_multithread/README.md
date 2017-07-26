## use modules generated with SWIG in a multi-thread environmentOriginally published: 2001-03-21 15:43:24 
Last updated: 2001-03-21 15:43:24 
Author: Joe VanAndel 
 
To use multiple threads, you must release the Python thread-lock.\nThe simplest way with SWIG is to use an except directive.For example,\nMark Hammond does the following in the Win32 extensions: