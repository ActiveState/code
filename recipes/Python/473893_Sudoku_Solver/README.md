## Sudoku Solver 
Originally published: 2006-02-15 18:44:04 
Last updated: 2006-03-14 07:52:29 
Author: Raymond Hettinger 
 
Yet another solver.  Uses knowns to eliminate possibilities, then tries assumptions from remaining possibilities (depth-first search with heuristic to first explore cells with the fewest unknowns).