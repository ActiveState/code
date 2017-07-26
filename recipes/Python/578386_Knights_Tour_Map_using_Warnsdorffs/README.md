## Knight's Tour Map using Warnsdorff's Algorithm  
Originally published: 2012-12-18 01:05:50  
Last updated: 2012-12-18 01:05:51  
Author: FB36   
  
Solves Knight's Tour Problem using Warnsdorff's Algorithm for every square on the chessboard of arbitrary size.\n\nIt colors each initial square with a color that depends on the final square coordinates.\n(This is a method used to create fractals.)\nMany different formulas maybe used for coloring (based on abs/rel x/y/dist/ang).\n\nCalculating each tour in full creates a highly chaotic image (and takes hours).\nSo I added maxItPercent to cut-off tours earlier.\n(Using %10 creates an image that has both ordered and chaotic regions.)