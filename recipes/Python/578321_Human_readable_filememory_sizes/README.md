## Human readable file/memory sizesOriginally published: 2012-11-04 10:27:00 
Last updated: 2012-11-05 11:59:20 
Author: Tony Flury 
 
In writing a application to display the file sizes of set of files, I wanted to provide a human readable size rather then just displaying a byte count (which can get rather big).\n\nI developed this useful short recipe that extends the format specifier mini Language to add the S presentation type - which will intelligently convert the value to be displayed into a known human readable size format - i.e. b, Kb,Mb, Gb etc. It honours the rest of the format specification language (http://docs.python.org/2/library/string.html#format-string-syntax)\n\nIt uses a factor of 1024 at each stage