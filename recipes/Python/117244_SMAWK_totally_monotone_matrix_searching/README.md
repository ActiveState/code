## SMAWK totally monotone matrix searching algorithm 
Originally published: 2002-03-17 18:04:31 
Last updated: 2002-03-17 18:04:31 
Author: David Eppstein 
 
This algorithm takes as input a function for computing matrix values, and searches for the position of maximum value in each row.  The matrix must satisfy the "totally monotone" property: in each submatrix (in particular each 2x2 submatrix) the positions of the maxima must move leftward as you go down the rows.  The algorithm uses this property to greatly reduce the number of matrix elements evaluated, compared to a naive algorithm that explicitly constructs the matrix.\n\nAs a simple example, we apply the algorithm to finding nearest neighbors in B for each point in A, where B may be distributed arbitrarily in space but the points of A lie along a single line.  Using SMAWK for this problem takes only linear time if the input is already sorted.