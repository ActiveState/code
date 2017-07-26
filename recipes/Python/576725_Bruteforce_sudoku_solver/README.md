## Brute-force sudoku solver  
Originally published: 2009-04-23 15:09:29  
Last updated: 2009-04-23 18:33:56  
Author: Sylvain Fourmanoit  
  
This is a very simple, short Sudoku solver using a classic brute-force approach.\n\nWhat makes it nice is the purely arithmetic one-liner computing the constraint c (the sequence of already used digits on the same row, same column, same block of a given cell).