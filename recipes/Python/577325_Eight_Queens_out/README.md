## Eight Queens With out Permutations

Originally published: 2010-07-21 10:11:20
Last updated: 2010-07-21 10:11:20
Author: Narayana Chikkam

Eight Queens is one of the popular algorithms in  backtracking. The solution given below uses simple math to reduce the processing. The logic is keep placing the coins on the board with below rules:\n1. Don't place the coin if there is another coin present in the same row\n2. Don't place the coin if there is another coin present in the same col\n3. Don't place the coin if there is another coin present in any of the diagonal lines.\n\nKeep repeating the above 3 rules recursively until we keep all the coins.\nProblem Definition: \nhttp://en.wikipedia.org/wiki/Eight_queens_puzzle