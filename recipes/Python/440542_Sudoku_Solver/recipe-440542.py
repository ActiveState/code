'''
Simple text based Sudoku solver.
'''
__author__ = 'Justin Shaw'

import copy

def uniqueInsert(l, v):
    '''
    Add v to list if it is not already there, else raise ValueError
    '''
    if v is not None:
        if v in l:
            raise ValueError('list already contains value %s' % v)
        assert 0 < v < 10, 'Only 1-9 allowed, got %s' % v
        l.append(v)
        
class Sudoku:
    def submat(self, i, j):
        '''
        Return i, j 3x3 submatrix of self.
        '''
        mat = self.mat
        out = []
        for srow_i in range(3):
            row = []
            for scol_i in range(3):
                v = mat[i * 3 + srow_i][j * 3 + scol_i]
                row.append(v)
            out.append(row)
        return out
    
    def copy(self):
        return Sudoku(copy.deepcopy(self.mat))
    
    def add(self, v, i, j):
        '''
        Fill in an entry in self.mat
        '''
        self.mat[i][j] = v
        uniqueInsert(self.rows[i], v)
        uniqueInsert(self.cols[j], v)
        sub_i = i // 3 * 3 + j // 3
        uniqueInsert(self.subs[sub_i], v)

    def __init__(self, mat):
        '''
        Create a new Sudoku instance.
        mat -- 9x9 array of digits 1-9
               or None if no value is known for that spot
        '''
        self.mat = mat

        # keep track of all values used in each row, column and sub-matrix.
        rows = [[] for i in range(9)]
        cols = [[] for i in range(9)]
        subs = [[] for i in range(9)]
        
        for row_i in range(9):
            for col_i in range(9):
                v = self.mat[row_i][col_i]
                uniqueInsert(rows[row_i], v)
                uniqueInsert(cols[col_i], v)
        for srow_i in range(3):
            for scol_i in range(3):
                sub = self.submat(srow_i, scol_i)
                for i in range(3):
                    for j in range(3):
                        v = sub[i][j]
                        sub_i = srow_i * 3 + scol_i
                        uniqueInsert(subs[sub_i], v)
        self.rows = rows
        self.cols = cols
        self.subs = subs
        
    def __repr__(self):
        out = ''
        for i in range(9):
            if i % 3 == 0:
                out += '+-------+-------+-------+\n'
            for j in range(9):
                if j % 3 == 0:
                    out += '| '
                v = self.mat[i][j]
                if v is not None:
                    out += '%1d ' % v
                else:
                    out +=  '  '
            out += '|\n'
        out += '+-------+-------+-------+\n'
        return out

    def solve(self):
        '''
        Solve for the unknown positions of the puzzle
        '''
        
        min_poss = 9 # Minimum possible number of choices for a cell
        done = True
        for i in range(9):
            for j in range(9):
                sub_i = i // 3 * 3 + j // 3 # sub-matrix index
                v = self.mat[i][j]
                if v:
                    pass
                else:
                    # not all values filled out so we are not done yet
                    done = False
                    all = set(range(1, 10))

                    # determine all possible values for this cell
                    possible = (all.difference(self.rows[i])
                                .difference(self.cols[j])
                                .difference(self.subs[sub_i]))

                    # see if we have run into a brick wall
                    if len(possible) == 0:
                        raise ValueError('Sudoku not solvable')
                    elif len(possible) < min_poss:
                        
                        # keep track of cell with smallest number of choices
                        min_poss = len(possible)
                        best = possible
                        min_i = i
                        min_j = j
        if done:
            out = self
        else:
            
            # Try these possibilities and recurse
            for b in best:
                print min_i, min_j, b
                trial = self.copy()
                trial.add(b, min_i, min_j)
                print trial
                try:
                    soln = trial.solve()
                    break
                except ValueError:
                    soln = None
            if soln is None:
                print self
                raise ValueError('Sudoku not solvable')
            out = soln
        return out
                
N = None
easy = [
    [7, N, N,   1, 5, N,   N, N, 8],
    [N, N, 4,   N, N, 2,   N, N, N],
    [N, N, N,   N, N, 4,   5, 6, N],

    [6, N, N,   N, N, N,   N, 2, 9],
    [5, N, 2,   N, N, N,   8, N, 4],
    [3, 4, N,   N, N, N,   N, N, 1],

    [N, 3, 8,   6, N, N,   N, N, N],
    [N, N, N,   2, N, N,   9, N, N],
    [1, N, N,   N, 8, N,   N, N, 3]
    ]

hard = [
    [N, 4, N,   N, N, 7,   9, N, N],
    [N, N, 8,   5, 3, 9,   N, N, N],
    [N, 6, N,   N, N, N,   2, N, 3],

    [N, N, N,   N, N, 2,   5, N, N],
    [N, 8, 6,   N, N, N,   1, 4, N],
    [N, N, 9,   8, N, N,   N, N, N],

    [6, N, 3,   N, N, N,   N, 9, N],
    [N, N, N,   9, 8, 6,   3, N, N],
    [N, N, 1,   4, N, N,   N, 6, N]
    ]


evil = [
    [4, 2, N,   N, N, N,   N, 1, N],
    [N, N, N,   5, 4, N,   N, 3, N],
    [N, N, 6,   N, N, 7,   N, N, N],

    [N, N, N,   N, N, N,   2, 7, 9],
    [N, 1, N,   N, N, N,   N, 6, N],
    [3, 4, 2,   N, N, N,   N, N, N],

    [N, N, N,   9, N, N,   3, N, N],
    [N, 6, N,   N, 3, 8,   N, N, N],
    [N, 8, N,   N, N, N,   N, 5, 7]
    ]

blank = [
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],

    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N],
    [N, N, N,   N, N, N,   N, N, N]
    ]

import time
easy = Sudoku(easy)
hard = Sudoku(hard)
evil = Sudoku(evil)
print
print 'easy'
print easy
time.sleep(2)
easy.solve()
print
print 'hard'
print hard
time.sleep(2)
hard.solve()
print
print 'evil'
print evil
print
time.sleep(2)
evil.solve()
