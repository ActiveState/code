## "tail -f" with inode monitor

Originally published: 2010-09-21 07:34:35
Last updated: 2010-09-21 07:37:38
Author: Denis Barmenkov

Sometimes tail -f launched for log file miss the point when program recreates log file.\nScript in this recipe monitors inode changes for specified file and restarts tail if needed.