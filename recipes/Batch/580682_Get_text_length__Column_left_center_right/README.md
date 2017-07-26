## Get text length - Column left center and right alignement  
Originally published: 2016-06-14 14:52:59  
Last updated: 2016-06-15 06:42:00  
Author: Antoni Gual  
  
The recipe parses some lines of text (separator=$), calculates the width of each column and prints the text in columns with lefr, right and center alignment. I have put the strlen and the alignment routines in separate procedures, to ease the reuse. The alignement procedures work in place, the result is returned in the same variable as the original string.