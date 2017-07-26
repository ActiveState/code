## Subprocess with async I/O pipes class 
Originally published: 2009-05-16 22:23:30 
Last updated: 2009-05-17 02:02:04 
Author: Mike Kazantsev 
 
Just stumbled upon the need to move data chunks between subprocesses in a non-linear way with some logic in-between, so tee(1) and fifo(7)'s weren't too good option.\nInspired by 440554, but rewritten from scratch to remove unnecessary delays due to sleep(3) calls and suboptimal try/sleep-based polling.\n