## Determine size of console window on Windows

Originally published: 2005-10-11 15:41:58
Last updated: 2006-04-29 20:26:33
Author: Alexander Belchenko

This recipe is Python implementation of few lines of C-code that get useful information about current working console on Windows. It may be useful for console application to proper formatting output. Recipe need ctypes package to be installed.\n\nThis is the second version of recipe. When use handle of stdout for determining size of console and connect output of program via pipe to another program (e.g. pager 'more') then you get default 80x25 size. In case of using handle of stderr for this purpose then pipe don't destroy actual size.