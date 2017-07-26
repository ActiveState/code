## dal_2.py  
Originally published: 2006-04-26 09:53:56  
Last updated: 2006-04-26 09:53:56  
Author: Stephen Chappell  
  
The class DAL2 provides a way to label
blocks on a hard drive while storing
such information on the hard drive
itself. The information is kept in the
BIT (Block Information Table) and is
written out to disk when appropriate.
Otherwise, the BIT is kept in memory
for efficiency. The hard disk is again
presented as a collection of blocks but
completely hides disk IO as a result of
Disk Abstraction Layer 1.