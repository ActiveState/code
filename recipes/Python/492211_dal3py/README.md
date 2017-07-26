## dal_3.py  
Originally published: 2006-04-26 10:01:43  
Last updated: 2006-04-26 10:01:43  
Author: Stephen Chappell  
  
Disk Abstraction Layer 3 provides a more
useful framework for secondary memory and
provides an abstract interface for
implementing a generic file system. It
renumbers the blocks on the hard drive to
start at block 1 so that block 0 can be
considered a NULL reference. At a lower
level, block 0 would be seen to be where
the OS can keep a seed for its random
number generator (interface provided).