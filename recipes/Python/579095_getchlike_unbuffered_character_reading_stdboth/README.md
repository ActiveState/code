## getch()-like unbuffered character reading from stdin on both Windows and UnixOriginally published: 2015-08-19 04:45:50 
Last updated: 2015-08-19 04:45:51 
Author: jwhite88  
 
A small utility class to read single characters from standard input, on both Windows and UNIX systems.  It provides a getch() function-like instance.\n\nThis extends the original script by adding a timeout necessary for another project.