## Build extension modules inplace with a Makefile  
Originally published: 2015-01-29 20:54:36  
Last updated: 2015-01-29 20:54:38  
Author: Zack Weinberg  
  
Do you find distutils to be poorly documented, overdesigned yet still inadequate, and far too difficult to do anything out of the ordinary with?  Do you find yourself wishing that you could just write a Makefile for your extension modules, if only you knew how to form the compile commands?

Then this tool is for you.  An example (GNU) makefile to use it with is embedded in the code; it assumes you save this program as `get-module-compile-cmds.py` in the same directory as the makefile. Tested with 2.7 and 3.4; may work with older versions as well.

Installation is not currently supported; patches welcome.