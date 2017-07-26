## Convert Byte Size to String Representation

Originally published: 2009-10-08 10:51:29
Last updated: 2012-04-13 19:55:07
Author: Stephen Chappell

In anticipation of creating large data structure, it appeared to be helpful if the users could get an idea of how much memory (RAM in particular) would be used while attempting to create a large, multidimensional array. In order to convert the calculated size into a precise, human-readable format, the follow code was devised. In order to convert a number into an equivalent representation of bytes, just call the "convert" function while providing the number as its argument. The other functions are currently public in case anyone else finds them useful.