## Read a text file backwards  
Originally published: 2002-04-12 22:31:38  
Last updated: 2002-04-12 22:31:38  
Author: Matt Billenstein  
  
This recipe provides a class which will read a text file in reverse...  It basically reads a block of data from the end of the file as a list and keeps popping items off of that everytime the readline() method is called.  When the block is exhausted, another block is read, and so forth...  This takes care of corner cases where a line is longer than the buffer or the file is smaller than the buffer, etc.