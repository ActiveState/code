## Convert strings like '5d' and '60s' to timedelta objects  
Originally published: 2011-10-06 14:06:10  
Last updated: 2011-10-06 14:06:54  
Author: Dan McDougall  
  
I wrote this little function for `[Gate One](http://vimeo.com/24857127)` (a web-based terminal emulator/SSH client)...  It converts strings in the format of <num><character> into timedelta objects.  It's not rocket science but maybe it'll save someone a few keystrokes :).  Besides that, it comes with a really nice Sphinx-ready (reStructuredText) docstring with complete doctests.