## ShortForm  
Originally published: 2005-01-22 03:07:33  
Last updated: 2005-01-22 03:07:33  
Author: jessw   
  
Short Form prevents the Python shell from printing out giant piles of text.\nIt is a hack that ties into the display system.  When you are working with a multi-megabyte text file, referenced under the name `txt`, which takes 10 minutes to be printed in full (if you accidentally type '>>> txt') it's really nice to have this.