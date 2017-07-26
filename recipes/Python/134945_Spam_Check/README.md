###Spam Check

Originally published: 2002-06-21 16:39:50
Last updated: 2002-06-21 23:46:45
Author: Frank Fejes

I get a lot of spam. :(  Unfortunately, much of this spam is not the good old 4-5k message trying to sell something...many contain attachments in the 80-150k size range.  Add to this the facts that I still live off a dialup line and my mail client (the otherwise amazing sylpheed) does not filter at the POP3 level and it's clear that I need to do something about it.  Hence this python applet.  It uses poplib to connect to a POP3 server, list messages greater than a given size (default is 50k), and then prompt for which messages to delete.  It's been pretty handy for me.