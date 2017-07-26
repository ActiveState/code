## Large File Sizes on 32 bit Windows

Originally published: 2001-10-12 11:45:11
Last updated: 2001-10-12 11:45:11
Author: John Nielsen

You can't use the os library to determine the size of large files on 32 bit Windows. It may not be obvious from the name, however, a win32 call to FindFiles, can provide a solution.