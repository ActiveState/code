## Read a text file by-paragraphOriginally published: 2001-07-17 04:46:03 
Last updated: 2001-08-15 16:47:48 
Author: Alex Martelli 
 
Text files are most often read by-line, with excellent direct Python support.  Sometimes we need to use other units, such as the paragraph -- a sequence of non-empty lines separated by empty lines.  Python doesn't support that directly, but, as usual, it's not too hard to add such functionality.