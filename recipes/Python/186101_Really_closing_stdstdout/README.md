## Really closing stdin, stdout, stderr 
Originally published: 2003-03-01 17:58:30 
Last updated: 2003-03-01 17:58:30 
Author: skip  
 
When creating daemons on Unix-like systems, it's typical to close or redirect stdin,\nstdout, and stderr.  This simple recipe demonstrates that it's not quite as obvious\nas it might first appear.