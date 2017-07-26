## Sync the system clock to the naval time server  
Originally published: 2006-08-26 07:08:54  
Last updated: 2006-08-26 20:38:42  
Author: Jason Letbetter  
  
This software gets the date from a naval time server and updates the system  clock for posix OS supporting the "date" command.  It also requires an internet connection.

WARNING: It will not work if your system clock is already off by more than 1 month.

TIP: Use kcron to schedule this script on a periodic basis.