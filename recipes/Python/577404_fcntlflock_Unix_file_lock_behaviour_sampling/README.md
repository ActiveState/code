## fcntl.flock() (Unix file lock) behaviour sampling scriptOriginally published: 2010-09-22 00:08:15 
Last updated: 2010-09-22 00:11:12 
Author: Jan Kaliszewski 
 
A quick *fcntl.flock(fcntl.LOCK_EX | fcntl.LOCK_NB)* call sampling script: with *one file object* (and descriptor) or *separate file objects* (and different descriptors) pointing to the same filesystem path -- with/without **threading** or **forking**.\n\nIt's rather exemplum-and-educational piece of code than utility-script, unless somebody has to few slots in their memory to remember that **flock** is file-descriptor-tacked (then quick run of the script can save web-searching) :)