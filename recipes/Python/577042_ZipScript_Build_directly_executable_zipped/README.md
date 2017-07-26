###ZipScript: Build a directly executable zipped Python script set

Originally published: 2010-02-11 01:25:18
Last updated: 2010-02-11 15:32:38
Author: Glenn 

This function will package a python script and additional python modules, in either source or compiled form. Either are directly executable by Python 2.7/3.1 or newer.\n\nUses make-like logic to only rebuild if something is newer than the previous build.