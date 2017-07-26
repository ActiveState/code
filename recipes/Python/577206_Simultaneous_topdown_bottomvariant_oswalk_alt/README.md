## Simultaneous topdown and bottomup variant of os.walk() (alt. title: "Delete .pyc files and empty directories recursively")  
Originally published: 2010-04-21 20:16:08  
Last updated: 2010-04-21 20:16:09  
Author: George Sakkis  
  
The standard lib os.walk() function provides a topdown parameter that determines whether entries are yielded in a top-down or a bottom-up order. Sometimes though you may want each directory yielded twice; once before any of its children directories (and recursively their descendants) are yielded and once after they are all yielded. The walk2() function below does this by yielding 4-tuples; the first 3 elements are the same yielded by os.walk() and the 4th is True the first time (topdown) and False the second (bottomup).

An example is deleting all .pyc files and empty directories under some root dir, but excluding specific directories (e.g. VCS specific dirs). The exclusion check should be done topdown (we don't want to descend into any directory that must be excluded) but the check for empty directories has to be done bottom up, since a directory containing only .pyc files will be non-empty initially but empty after removing the files.