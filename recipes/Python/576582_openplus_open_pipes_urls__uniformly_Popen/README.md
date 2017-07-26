## openplus(): open pipes, urls ... uniformly with Popen, urlopen ... open 
Originally published: 2008-12-11 04:23:42 
Last updated: 2008-12-11 05:40:15 
Author: denis  
 
openplus() opens pipes and some other objects that quack like files,\nas well as files:\n\n    | pipe ...  -- Popen() a shell\n    http:// ftp:// ...  -- urlopen()\n    `ls $x`, `geturl web data`  -- shell -> filename or url\n    ~/a/b       -- sh ls\n    .gz         -- gunzip\n    -           -- stdin / stdout\n    else        -- the builtin open()\n\nUsers can then read e.g.\n    "| filter data | sort"\n    "| convert ... xx.jpg"\n    "\\`geturl web data\\`"\nlike files, just by importing openplus and changing open() -> openplus().