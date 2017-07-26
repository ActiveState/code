## Proof-of-concept for a more space-efficient, faster-looping dictionary

Originally published: 2012-12-10 00:39:57
Last updated: 2013-01-17 09:28:24
Author: Raymond Hettinger

Save space and improve iteration speed by moving the hash/key/value entries to a densely packed array keeping only a sparse array of indices.  This eliminates wasted space without requiring any algorithmic changes.