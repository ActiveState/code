## Super Simple Sudoku Solver in Python source code  
Originally published: 2012-05-19 14:50:23  
Last updated: 2012-06-23 14:56:05  
Author: David Adler  
  
A simple algorithm which uses a recursive function to solve the puzzle.
_____________
THE ALGORITHM

The credit for this algorithm must go to Richard Buckland:
http://www.youtube.com/watch?v=bjObm0hxIYY&feature=autoplay&list=PL6B940F08B9773B9F&playnext=1

Takes a partially filled in grid, inserts the min value in a cell (could be a random cell, in this case the first free cell). If the min value is not legal it will increment until the max value is reached (number 9), checking each time if the incremented value is legal in that cell (ie does not clash with any already entered cells in square, col or row). If it is legal, it will call itself (the hasSolution function) thus using this slightly more filled in grid to find a new cell and check which value is legal in this next cell. If no values are legal in the next cell, it will clear the previous grid entry and try incrementing the value.

isLegal = does not conflict with any other numbers in the same row, column or square