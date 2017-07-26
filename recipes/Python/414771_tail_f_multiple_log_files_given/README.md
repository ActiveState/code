## tail -f for multiple log files in a given directory  
Originally published: 2005-05-20 08:12:01  
Last updated: 2005-05-20 16:23:54  
Author: Bibha Tripathi  
  
I needed to write a Python script for a "tail -f" that displays log entries from multiple files in a given directory. The display had to be in chronological order, the first column of each log file being timestamp of the log. It should work for any type of files.

Usage:  python tail_m.py directoryname