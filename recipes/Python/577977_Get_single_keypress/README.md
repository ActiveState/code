## Get single keypressOriginally published: 2011-12-06 08:46:32 
Last updated: 2011-12-06 08:46:33 
Author: Steven D'Aprano 
 
Here's a platform-independent module that exposes a single function, getch, which reads stdin for a single character. It uses msvcrt.getch on Windows, and should work on any platform that supports the tty and termios modules (e.g. Linux).\n\nThis has been tested on Python 2.4, 2.5 and 2.6 on Linux.