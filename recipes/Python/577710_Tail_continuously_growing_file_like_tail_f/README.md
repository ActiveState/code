## Tail a continuously growing file (like tail -f filename) 
Originally published: 2011-05-20 16:25:54 
Last updated: 2011-05-20 16:32:59 
Author: Jason Morriss 
 
This is my version of a "File Tail" class for Python3 (will not work on Python2 w/o a couple of modifications). My original inspiration came from the perl File::Tail module.\n\nTransparently handles files that get rotated or truncated. \n* Does not take 100% CPU. \n* Does not take up much memory.\n* Is capable of handling any size log file.\n* *Not tested on Windows*\n\nExample:\n\n    from filetail import FileTail\n    tail = FileTail("/var/log/syslog")\n    for line in tail:\n        print(line, end="")\n