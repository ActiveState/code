## dal_2.py

Originally published: 2006-04-26 09:53:56
Last updated: 2006-04-26 09:53:56
Author: Stephen Chappell

The class DAL2 provides a way to label\nblocks on a hard drive while storing\nsuch information on the hard drive\nitself. The information is kept in the\nBIT (Block Information Table) and is\nwritten out to disk when appropriate.\nOtherwise, the BIT is kept in memory\nfor efficiency. The hard disk is again\npresented as a collection of blocks but\ncompletely hides disk IO as a result of\nDisk Abstraction Layer 1.