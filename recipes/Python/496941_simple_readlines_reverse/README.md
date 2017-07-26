## simple readlines in reverse w/deque 
Originally published: 2006-08-04 08:04:03 
Last updated: 2006-08-04 19:09:16 
Author: John Nielsen 
 
This a very simple implementation for how to do a readlines in reverse. It is not optimized for performance (which often doesn't matter). I have a 2nd version that is faster by loading blocks of data into memory instead of character by character. Of course, the code then almost doubles in size. And finally a third version that is the fastest, using split.