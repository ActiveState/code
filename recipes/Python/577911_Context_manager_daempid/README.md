## Context manager for a daemon pid fileOriginally published: 2011-10-17 12:41:57 
Last updated: 2013-10-07 21:03:30 
Author: Graham Poulter 
 
Context manager for a pid (process id) file used to tell whether a daemon process is still running.\n\nOn entry, it writes the pid of the current process to the path.  On exit, it removes the file.\n\nDesigned to work with python-daemon.\n