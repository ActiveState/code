## Recursive file/folder cleaner  
Originally published: 2009-02-04 03:19:39  
Last updated: 2011-02-12 20:30:59  
Author: Alia Khouri  
  
This script recursively scans a given path and applies a cleaning 'action' 
to matching files and folders. By default files and folders matching the 
specified (.endswith) patterns are deleted. Alternatively, _quoted_ glob
patterns can used with the '-g' or '--glob' option.

By design, the script lists targets and asks permission before applying 
cleaning actions. It should be easy to extend this script with further 
actions and also more intelligent pattern matching functions.

The getch (single key confirmation) functionality comes courtesy of 
http://code.activestate.com/recipes/134892/

To use it, place the script in your path and call it something like 'clean':

    Usage: clean [options] patterns
        
            deletes files/folder patterns:
                clean .svn .pyc
                clean -p /tmp/folder .svn .csv .bzr .pyc
                clean -g "*.pyc"
                clean -ng "*.py"
    
            converts line endings from windows to unix:
                clean -e .py
                clean -e -p /tmp/folder .py

    Options:
      -h, --help            show this help message and exit
      -p PATH, --path=PATH  set path
      -n, --negated         clean everything except specified patterns
      -e, --endings         clean line endings
      -g, --glob            clean with glob patterns
      -v, --verbose         

