## A Simple Timing Function  
Originally published: 2013-12-01 01:37:27  
Last updated: 2013-12-01 01:39:44  
Author: Mike Sweeney  
  
This function prints out a message with the elapsed time from the 
previous call. It works with most Python 2.x platforms. The function 
uses a simple trick to store a persistent variable (clock) without
using a global variable.