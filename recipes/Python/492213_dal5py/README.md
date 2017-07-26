## dal_5.py  
Originally published: 2006-04-26 10:20:16  
Last updated: 2006-04-26 10:20:16  
Author: Stephen Chappell  
  
DAL5 continues to refine the file system's
interface and provides methods that should
look similar to what most programmers are
used to working with. Files have still not
been completely abstracted away and all
path names must be given as relative to
the root. The path separator is defined
in this module along with a list of
characters for valid file and directory names.