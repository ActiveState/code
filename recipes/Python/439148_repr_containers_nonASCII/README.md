## repr() of containers with non-ASCII stringsOriginally published: 2005-08-12 02:53:35 
Last updated: 2005-08-12 02:53:35 
Author: Christos Georgiou 
 
Printing sequences or maps containing non-ASCII strings results in escape sequences.  This function uses the not-so-commonly-known "string_escape" codec to facilitate printing such sequences for quick-viewing.