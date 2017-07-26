## printing a banner/title lineOriginally published: 2004-10-02 12:28:30 
Last updated: 2010-07-07 17:20:35 
Author: Trent Mick 
 
Sometimes it is nice to print a banner line in the output of a command line script  to group a section of output (say, in a log file). This little banner() function will center a given string in a line (using a character and length you can specify).\n\n**Update**: Just use `string.center(...)` ([docs](http://docs.python.org/library/string.html#string.center)) as suggested in the comments below.\n