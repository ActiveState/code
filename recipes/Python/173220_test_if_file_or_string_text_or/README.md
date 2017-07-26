## test if a file or string is text or binary  
Originally published: 2003-01-10 13:37:35  
Last updated: 2003-01-11 01:13:40  
Author: Andrew Dalke  
  
Here's a quick test to see if a file or string contains text or is binary.  The difference between text and binary is ill-defined, so this duplicates the definition used by Perl's -T flag, which is:\n<br/>\n The first block or so of the file is examined for odd characters such as strange control codes or characters with the high bit set. If too many strange characters (>30%) are found, it's a -B file, otherwise it's a -T file. Also, any file containing null in the first block is considered a binary file.