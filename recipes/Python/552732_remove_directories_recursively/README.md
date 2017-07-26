## remove directories recursively  
Originally published: 2008-03-26 16:14:58  
Last updated: 2008-03-26 16:14:58  
Author: Dan Gunter  
  
Extremely simple bit of code to remove a directory recursively.\nSimply feed it the path of the top-level directory to remove, and off it goes.\nAs presented, there is no error-checking; failure at any point will stop the function and raise an IOError.