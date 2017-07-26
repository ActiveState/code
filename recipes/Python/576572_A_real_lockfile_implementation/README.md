## A real lockfile implementation 
Originally published: 2008-11-26 00:58:40 
Last updated: 2008-11-26 00:58:40 
Author: Aaron Gallagher 
 
Because I didn't see a good implementation, I've posted here my own implementation of a lockfile context manager. It's POSIX-only because I don't have a Windows machine to test cross-platform atomicity on. Sorry about that.