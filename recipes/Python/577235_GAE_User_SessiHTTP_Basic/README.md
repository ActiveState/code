## GAE User Session with HTTP Basic Authentication  
Originally published: 2010-05-20 20:31:02  
Last updated: 2010-05-20 23:49:49  
Author: Berend   
  
HTTP Basic is an unsecure but easy to implement authentication protocol. I think its good enough for a simple client in front of an SSL capable server. Google App-Engine supports SSL, and here is a recipe to set up the user-session using HTTP Basic. 

gauth has the code from my not-really-a-recipe listing at: 
http://code.activestate.com/recipes/577217-routines-for-programmatically-authenticating-with-