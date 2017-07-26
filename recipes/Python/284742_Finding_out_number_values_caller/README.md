## Finding out the number of values the caller is expecting  
Originally published: 2004-05-19 11:43:44  
Last updated: 2004-05-21 13:13:35  
Author: Sami Hangaslammi  
  
Sometimes you might want to make a function behave differently if the caller is expecting one or several values (e.g. x=func() versus x,y=func()). The expecting() function lets the function implementer find out how many values the caller wants as a function result.