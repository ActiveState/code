## Timing various python statements 
Originally published: 2008-02-06 00:13:09 
Last updated: 2008-02-06 00:13:09 
Author: Oliver Schoenborn 
 
The timeit module (in Python standard library) is handy to find out how fast a statement takes to execute, but not very convenient to compare speed of several equivalent statements: too much typing, need to create a Timer object for each statement, etc, tedious. The timings module provides the times() function to make it super easy to compare several statements in one call.