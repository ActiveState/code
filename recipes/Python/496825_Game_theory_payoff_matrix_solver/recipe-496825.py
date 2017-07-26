''' Approximate the strategy oddments for 2 person zero-sum games of perfect information.

Applies the iterative solution method described by J.D. Williams in his classic
book, The Compleat Strategyst, ISBN 0-486-25101-2.   See chapter 5, page 180 for details. '''

from operator import add, neg

def solve(payoff_matrix, iterations=100):
    'Return the oddments (mixed strategy ratios) for a given payoff matrix'
    transpose = zip(*payoff_matrix)
    numrows = len(payoff_matrix)
    numcols = len(transpose)
    row_cum_payoff = [0] * numrows
    col_cum_payoff = [0] * numcols
    colpos = range(numcols)
    rowpos = map(neg, xrange(numrows))
    colcnt = [0] * numcols
    rowcnt = [0] * numrows
    active = 0
    for i in xrange(iterations):
        rowcnt[active] += 1        
        col_cum_payoff = map(add, payoff_matrix[active], col_cum_payoff)
        active = min(zip(col_cum_payoff, colpos))[1]
        colcnt[active] += 1       
        row_cum_payoff = map(add, transpose[active], row_cum_payoff)
        active = -max(zip(row_cum_payoff, rowpos))[1]
    value_of_game = (max(row_cum_payoff) + min(col_cum_payoff)) / 2.0 / iterations
    return rowcnt, colcnt, value_of_game

###########################################
# Example solutions to two pay-off matrices
      
print solve([[2,3,1,4], [1,2,5,4], [2,3,4,1], [4,2,2,2]])   # Example on page 185
print solve([[4,0,2], [6,7,1]])                             # Exercise 2 number 3
