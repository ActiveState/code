###Watching a directory tree on Unix

Originally published: 2003-08-11 18:23:58
Last updated: 2003-08-11 18:23:58
Author: A.M. Kuchling

The watch_directories() function takes a list of paths and a callable object, and then repeatedly traverses the directory trees rooted at those paths, watching for files that get deleted or have their modification time changed.  The callable object is then passed two lists containing the files that have changed and the files that have been removed.