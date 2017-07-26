## remove directories recursively  
Originally published: 2008-03-26 16:14:58  
Last updated: 2008-03-26 16:14:58  
Author: Dan Gunter  
  
Extremely simple bit of code to remove a directory recursively.
Simply feed it the path of the top-level directory to remove, and off it goes.
As presented, there is no error-checking; failure at any point will stop the function and raise an IOError.