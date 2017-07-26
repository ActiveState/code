## Simple MultiThreaded Timer Job ControllerOriginally published: 2009-05-11 02:03:52 
Last updated: 2009-05-11 02:05:16 
Author: sumerc  
 
We have tried to write an audit for our server to check our server's connection, status and other internal info and there are multiple threads invoking multiple tasks. So I came up with this simple utility that takes a job and runs it in a specific interval.