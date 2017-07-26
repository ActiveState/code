## Non-blocking readlines()  
Originally published: 2014-06-30 20:30:56  
Last updated: 2014-06-30 20:30:57  
Author: Zack Weinberg  
  
A generator function which takes a file object (assumed to be some sort of pipe or socket, open for reading), and yields lines from it without blocking.  If there is no input available, it will yield an endless stream of empty strings until input becomes available again; caller is responsible for not going into a busy loop.  (Newlines are normalized but not stripped, so if there is actually a blank line in the input, the value yielded will be `'\n'`.)  The intended use case is a thread which must respond promptly to input from a pipe, and also something else which cannot be fed to `select` (e.g. a `queue.Queue`).  Note that the file object is ignored except for its `fileno`.

Only tested on Unix.  Only tested on 3.4; ought to work with any python that has `bytearray`, `locale.getpreferredencoding`, and `fcntl`.