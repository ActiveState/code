#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sudoku game maker

"""

__author__ = 'Ripley6811'
__contact__ = 'python at boun.cr'
__copyright__ = ''
__license__ = ''
__date__ = 'Thu Aug 30 10:09:06 2012'
__version__ = '0.1'

#===============================================================================
# IMPORT STATEMENTS
#===============================================================================
from numpy import * 

#===============================================================================
# METHODS
#===============================================================================

def new_block():
    return random.permutation(arange(1,10)).reshape(3,3)

def test_rowcol(S):
    retval = True
    for row in S:
        if len(set(row).difference([0])) < count_nonzero(row):
            retval = False
            break
    for col in S.T:
        if len(set(col).difference([0])) < count_nonzero(col):
            retval = False
            break
    return retval



def generate_grid(S=None, verbose=False):
    #PART 1: SET FIRST THREE ROWS AND FIRST THREE COLUMNS
    available = set(range(1,10))
    if S == None:
        S = new_block()
        if verbose: print S
        while True:
            Srow = append(append(S,new_block(),1),new_block(),1)
            if test_rowcol(Srow):
                if verbose: print Srow
                break
        while True:
            Scol = append(append(S,new_block(),0),new_block(),0)
            if test_rowcol(Scol):
                Scol = append(Scol[3:],zeros((6,6),int),1)
                if verbose: print Scol
                break
        S = append(Srow,Scol,0)
    #PART 2: FILL IN THE REST OF GRID FROM PART 1. [3:,3:]
    if verbose: print '.',
    while True:
        S[3:6,3:6] = new_block()
        if test_rowcol(S[:6,:6]):
            break
    while True:
        S[6:,6:] = new_block()
        if test_rowcol(S):
            break
    for i in range(3,9):
        for j in range(3,9):
            if S[i,j] == 0:
                subset = available.difference( set(S[i]) ).difference( set(S[:,j]) )
                if len(subset) == 1:
                    S[i,j] = subset.pop()
                else:
                    S[3:,3:] = 0
                    return generate_grid(S, verbose)
    if verbose: print '\n', S
    return S

def reduce_options(board, Pcube):

    row,col = where(board == 0)
    playoption = []
    for i in range(9):
        for j in range(9):
            if board[i,j] != 0:
                Pcube[i,j,Pcube[i,j]!=board[i,j]] *= 0

    for i,j in zip(row,col):
        exclude = set(board[i])
        exclude = exclude.union(board[:,j])
        exclude = exclude.union(board[i/3*3:i/3*3+3,j/3*3:j/3*3+3].flat)
        for each in exclude:
            Pcube[i,j,Pcube[i,j]==each] = 0

    for layer in Pcube.T: # probable layers 1 through 9
        for i in range(9):
            rowsfilled = sum(layer[i,:3])>0, sum(layer[i,3:6])>0, sum(layer[i,6:])>0
            if sum(rowsfilled) == 1:
                rowsfilled = repeat(rowsfilled,3)
                layer[i/3*3+(i+1)%3,rowsfilled] *= 0
                layer[i/3*3+(i+2)%3,rowsfilled] *= 0
        layer = layer.T
        for i in range(9):
            rowsfilled = sum(layer[i,:3])>0, sum(layer[i,3:6])>0, sum(layer[i,6:])>0
            if sum(rowsfilled) == 1:
                rowsfilled = repeat(rowsfilled,3)
                layer[i/3*3+(i+1)%3,rowsfilled] *= 0
                layer[i/3*3+(i+2)%3,rowsfilled] *= 0


#    print str(Pcube.T).replace('0','~')

    for i,j in zip(row,col):
        if count_nonzero(Pcube[i,j]) == 1:
            playoption.append( (i,j,sum(Pcube[i,j])) )
    return playoption


def generate_game(S, verbose=False):
    gametest = S.copy()

    for each in range(200):
        i = random.randint(81)
        temp = gametest.flat[i]
        gametest.flat[i] = 0

        if not isSolvable(gametest):
            gametest.flat[i] = temp
    return gametest


def isSolvable(testgame):
    board = testgame.copy()
    P = ones((9,9,9),int)
    for i in arange(9):
        P[:,:,i] *= i+1
    print 'GAME\n', str(board).replace('0','_')
    playorder = []
    laststate = sum(P)
    while sum(board == 0) > 0:
        #REDUCE OPTIONS FOR EACH HOLE
        playoptions = reduce_options(board, P)
        print playoptions
#        print str(board).replace('0','_')
        for i,j,v in playoptions:
            board[i,j] = v
        thisstate = sum(P)
        if thisstate == laststate:
            break
        else:
            laststate = thisstate
    return True if sum(board == 0) == 0 else False




def main():
    """Description of main()"""
    solution = generate_grid(verbose=True)
    sudoku = generate_game(solution, verbose=True)
    print 'Solution\n', solution
    print 'Sudoku\n', str(sudoku).replace('0','_')
    print sum(sudoku == 0), 'blanks (', int(sum(sudoku == 0)/.81), '%)'


if __name__ == '__main__':
    main()
