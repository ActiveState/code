## Star Mapper  
Originally published: 2006-03-26 12:45:44  
Last updated: 2006-03-26 12:45:44  
Author: Stephen Chappell  
  
The following recipe demonstrates the use of SETs in Python.
The scenario that this was written for is as follows:

A star map is given according to the format X,Y,Z|...|X,Y,Z:
X represents the X coordinate of the star (which may be any real integer).
Y represents the Y coordinate on the star (which may be any real integer).
Z represents the color of the star (which may be any real integer larger than 0).
| separates the stars (strings represented by X,Y,Z).
, separates the numbers describing the stars (X,Y,Z).
: represents the end of the star map string.
... is an arbitrary number of X,Y,Z strings with appropriate pipes.

The problem involves finding all constellations that are shared across two
different star maps. A constellation is defined as a group of stars. When trying
to find out if a constellation is shared by two star maps, color and position do
not matter. However, all constellations would be oriented in the same direction.