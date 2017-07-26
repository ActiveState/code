###Set windows 7 to lock itself (upon timeout) if no internet connection found - security measure

Originally published: 2012-07-09 20:45:32
Last updated: 2012-07-09 20:56:22
Author: commentator8 

This script (or exe if using web2py with """setup(windows=['locker2.py']))""") can be run as a task in windows every x minutes and will test for the presence of an internet connection and depending on whether it is found will set windows to lock after a given timeout without user activity.\n\nThis was made with help from random code snippets from around the web.\n\nTested only on windows 7.