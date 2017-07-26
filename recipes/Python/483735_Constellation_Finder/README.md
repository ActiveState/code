## Constellation Finder  
Originally published: 2006-04-06 15:35:21  
Last updated: 2006-04-06 22:42:16  
Author: Stephen Chappell  
  
The following recipe demonstrates the use of SETs in Python.
The scenario that this was written for is as follows:

A star map is given according to the format X,Y,Z|...|X,Y,Z:
X represents the X coordinate of the star (which may be any real integer).
Y represents the Y coordinate on the star (which may be any real integer).
Z represents the color of the star (which may be any real integer larger than 0).
| separates the stars (strings represented by X,Y,Z).
, separates the numbers describing the stars (X,Y,Z).
: represents the end of the star map.
... is an arbitrary number of X,Y,Z strings with appropriate pipes.

As an extention to the original problem that this code was written for,
constellation definitions can follow the colon. The constellation string
that might follow is described by the following:

:C!D#...#D|...|C!D#...#D
: represents the beginning of the constellation definitions.
C!D#...#D represents one constellation definition.
| is the constellation definition separator.
C is a number that identifies what constellation is being defined.
D can be repesented as X,Y;X,Y or X,Y.
X would be the X coordinate of a star defined in the star map.
Y would be the Y coordinate of a star defined in the star map.
, would be the coordinate separator.
; would be the star separator.
... would be an arbitrary number of D string with appropriate # signs.
... would be an arbitrary number of constellation definitions.

The explanation for D is that if two stars are listed, they are joined
together with a line segment; but if there is one star, it is only highlighted.

In this updated version of the code, there is a key object that has
constellations already identified and a stars object that contains
the stars in the sky. Keys are used to unlocks the stars and the
results are printed out for the user of the program.