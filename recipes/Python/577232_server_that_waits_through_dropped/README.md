## A server that waits through dropped connectionsOriginally published: 2010-05-19 18:36:11 
Last updated: 2010-05-19 18:37:10 
Author: Kaushik Ghose 
 
The code is a barebones example of how to write a loop for a server so that it gracefully detects when the client has dropped the connection and goes back to listening for a new client.