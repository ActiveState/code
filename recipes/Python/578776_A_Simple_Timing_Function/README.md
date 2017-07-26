## A Simple Timing FunctionOriginally published: 2013-12-01 01:37:27 
Last updated: 2013-12-01 01:39:44 
Author: Mike Sweeney 
 
This function prints out a message with the elapsed time from the \nprevious call. It works with most Python 2.x platforms. The function \nuses a simple trick to store a persistent variable (clock) without\nusing a global variable.