## openplus(): open pipes, urls ... uniformly with Popen, urlopen ... open  
Originally published: 2008-12-11 04:23:42  
Last updated: 2008-12-11 05:40:15  
Author: denis   
  
openplus() opens pipes and some other objects that quack like files,
as well as files:

    | pipe ...  -- Popen() a shell
    http:// ftp:// ...  -- urlopen()
    `ls $x`, `geturl web data`  -- shell -> filename or url
    ~/a/b       -- sh ls
    .gz         -- gunzip
    -           -- stdin / stdout
    else        -- the builtin open()

Users can then read e.g.
    "| filter data | sort"
    "| convert ... xx.jpg"
    "\`geturl web data\`"
like files, just by importing openplus and changing open() -> openplus().