## Tail a continuously growing file (like tail -f filename)  
Originally published: 2011-05-20 16:25:54  
Last updated: 2011-05-20 16:32:59  
Author: Jason Morriss  
  
This is my version of a "File Tail" class for Python3 (will not work on Python2 w/o a couple of modifications). My original inspiration came from the perl File::Tail module.

Transparently handles files that get rotated or truncated. 
* Does not take 100% CPU. 
* Does not take up much memory.
* Is capable of handling any size log file.
* *Not tested on Windows*

Example:

    from filetail import FileTail
    tail = FileTail("/var/log/syslog")
    for line in tail:
        print(line, end="")
