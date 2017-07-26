## dal_3.py

Originally published: 2006-04-26 10:01:43
Last updated: 2006-04-26 10:01:43
Author: Stephen Chappell

Disk Abstraction Layer 3 provides a more\nuseful framework for secondary memory and\nprovides an abstract interface for\nimplementing a generic file system. It\nrenumbers the blocks on the hard drive to\nstart at block 1 so that block 0 can be\nconsidered a NULL reference. At a lower\nlevel, block 0 would be seen to be where\nthe OS can keep a seed for its random\nnumber generator (interface provided).