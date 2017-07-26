#!/usr/bin/env python

"""
loader.py - From a directory name:

1: append the directory to the sys.path
2: find all modules within that directory
3: import all modules within that directory
4: filter out built in methods from those modules
5: return a list of useable methods from those modules

Allows the user to import a series of python modules without "knowing" anything
about those modules.

Copyright 2005 Jesse Noller <jnoller@gmail.com>

"""

import os, sys

def import_libs(dir):
    """ Imports the libs, returns a list of the libraries. 
    Pass in dir to scan """
    
    library_list = [] 
    
    for f in os.listdir(os.path.abspath(dir)):       
        module_name, ext = os.path.splitext(f) # Handles no-extension files, etc.
        if ext == 'py': # Important, ignore .pyc/other files.
            print 'imported module: %s' % (module_name)
            module = __import__(module_name)
            library_list.append(module)
 
    return library_list

###############################################################################

def filter_builtins(module):
    """ Filter out the builtin functions, methods from module """

    # Default builtin list    
    built_in_list = ['__builtins__', '__doc__', '__file__', '__name__']
    
    # Append anything we "know" is "special"
    # Allows your libraries to have methods you will not try to exec.
    built_in_list.append('special_remove')

    # get the list of methods/functions from the module
    module_methods = dir(module) # Dir allows us to get back ALL methods on the module.

    for b in built_in_list:
        if b in module_methods:
            module_methods.remove(b)

    print module_methods
    return module_methods

###############################################################################

def main(dir):

    if os.path.isdir(dir):
        sys.path.append(dir)
    else:
        print '%s is not a directory!' % (dir)
    
    lib_list = import_libs(dir)
    
    for l in lib_list:
        filter_builtins(l)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "error: missing directory name"
        sys.exit(1)
    else:
        main(sys.argv[1])
