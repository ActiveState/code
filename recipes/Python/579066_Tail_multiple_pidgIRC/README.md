## Tail multiple pidgin IRC logfiles  
Originally published: 2015-06-03 09:55:04  
Last updated: 2015-06-06 12:13:00  
Author: Anton Vredegoor  
  
Tail multiple pidgin IRC logfiles. \n\nPidgin should be connected to IRC with the channels one\nwants to tail joined, and it should save logs as text.\n\nThe script needs two arguments:\n\n    the directory containing the directories with channel logs\n\n    a list of channel names, quoted and separated by spaces\n\nExample command:\n\npython pidgin-irctail.py \n    -d ~/.purple/logs/irc/YOUR_IRC_HANDLE@irc.freenode.net \n    -c "#chan1 #chan2 #chan3"\n\nSome text elements are higlighted, and channel names are\ninserted into the log lines after the time info.\n\nIf more than one channel is entered, the output of the logs\nis merged. \n