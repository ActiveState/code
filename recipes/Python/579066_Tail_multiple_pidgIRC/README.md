## Tail multiple pidgin IRC logfiles  
Originally published: 2015-06-03 09:55:04  
Last updated: 2015-06-06 12:13:00  
Author: Anton Vredegoor  
  
Tail multiple pidgin IRC logfiles. 

Pidgin should be connected to IRC with the channels one
wants to tail joined, and it should save logs as text.

The script needs two arguments:

    the directory containing the directories with channel logs

    a list of channel names, quoted and separated by spaces

Example command:

python pidgin-irctail.py 
    -d ~/.purple/logs/irc/YOUR_IRC_HANDLE@irc.freenode.net 
    -c "#chan1 #chan2 #chan3"

Some text elements are higlighted, and channel names are
inserted into the log lines after the time info.

If more than one channel is entered, the output of the logs
is merged. 
