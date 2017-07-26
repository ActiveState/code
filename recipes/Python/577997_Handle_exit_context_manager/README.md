## Handle exit context manager

Originally published: 2011-12-27 15:04:37
Last updated: 2014-08-01 08:28:07
Author: Giampaolo Rodolà

A context manager which properly handles SIGTERM (SystemExit) and SIGINT (KeyboardInterrupt) signals, registering a function which is always guaranteed to be called on interpreter exit.\nAlso, it makes sure to execute previously registered functions as well (if any).