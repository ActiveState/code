###Recoursive File Moving

Originally published: 2010-09-28 17:41:58
Last updated: 2010-09-28 19:01:24
Author: shawn 

This script is placed in a location then run.  All files underneath the root will be propagated to the top level, while deleting any old directory's.\n\nProblems: If you have large files in nested folders you will be copying them multiple times.\n\np.s. shoulda used walk() but i'm newb