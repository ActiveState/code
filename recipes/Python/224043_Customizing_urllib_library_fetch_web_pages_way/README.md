## Customizing the urllib library to fetch web pages the way you want  
Originally published: 2003-09-22 08:02:29  
Last updated: 2003-09-22 08:02:29  
Author: Dmitri Fours  
  
Problem:
You want to use urllib to fetch web pages.
You are not able to do it with the standard library functionality.

Solution:
Intercept the urllib.URLopener method.