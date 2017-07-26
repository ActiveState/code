## Rsync Algorithm  
Originally published: 2010-12-26 01:33:37  
Last updated: 2011-01-09 16:32:22  
Author: Eric Pruitt  
  
This is a pure Python implementation of the [rsync algorithm](http://samba.anu.edu.au/rsync/). On my desktop (3.0GHz dual core, 7200RPM), best case throughput for target file hash generation and delta generation is around 2.9MB/s. Absolute worst case scenario (no blocks in common) throughput for delta generation is 200KB/s to 300KB/s on the same system.\n\nTested in Python 2.5, 2.6, and 3.1. In 2.7, io.BufferedReader should yield the best throughput. On all other versions use __builtin__.open.