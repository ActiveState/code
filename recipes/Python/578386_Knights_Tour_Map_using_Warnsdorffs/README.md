## Knight's Tour Map using Warnsdorff's Algorithm  
Originally published: 2012-12-18 01:05:50  
Last updated: 2012-12-18 01:05:51  
Author: FB36   
  
Solves Knight's Tour Problem using Warnsdorff's Algorithm for every square on the chessboard of arbitrary size.

It colors each initial square with a color that depends on the final square coordinates.
(This is a method used to create fractals.)
Many different formulas maybe used for coloring (based on abs/rel x/y/dist/ang).

Calculating each tour in full creates a highly chaotic image (and takes hours).
So I added maxItPercent to cut-off tours earlier.
(Using %10 creates an image that has both ordered and chaotic regions.)