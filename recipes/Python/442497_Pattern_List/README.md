## Pattern List  
Originally published: 2005-10-31 04:54:30  
Last updated: 2005-10-31 04:54:30  
Author: mark williamson  
  
I found my self want to express -string- in -list of regular expressions- and so I wrote this quick object to do the trick for me. It takes a list of strings containing regular expressions, compiles them into an internal list and then using the __contains__ operation ("in") looks to see if a given string contains any of the expressions. The first success returns True otherwise it returns False.