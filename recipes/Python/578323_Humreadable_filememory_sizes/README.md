## Human readable file/memory sizes v2 
Originally published: 2012-11-10 23:06:26 
Last updated: 2012-11-11 17:28:57 
Author: Tony Flury 
 
In writing a application to display the file sizes of set of files, I wanted to provide a human readable size rather then just displaying a byte count (which can get rather big).\n\nI developed this useful short recipe that extends the format specifier mini Language to add new presentation type s- which will intelligently convert the value to be displayed into a known human readable size format - i.e. b, Kb,Mb, Gb, B, KB  etc. It honours the rest of the format specification language (http://docs.python.org/2/library/string.html#format-string-syntax)\n\nIt uses a factor of 1024 for IEC and common formats, and factor of 1000 for SI units.