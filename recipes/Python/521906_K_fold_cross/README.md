###K fold cross validation partition

Originally published: 2007-06-14 00:59:57
Last updated: 2007-06-16 08:57:51
Author: John Reid

Takes a sequence and yields K partitions of it into training and validation test sets. Training sets are of size (k-1)*len(X)/K and partition sets are of size len(X)/K