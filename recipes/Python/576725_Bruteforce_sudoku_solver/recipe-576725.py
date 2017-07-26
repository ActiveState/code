'''
Brute-force, backtracking Sudoku solver in about fifteen lines.

Works on Python 2.6 and Python 3.
'''
def solve(s):
    ''' 
    Solve a Sudoku:

    - Accepts s, a sequence of 81 integers from 0 to 9 in row of
    column order, zeros indicating the cells to fill.

    - Returns the first found solution as a sequence of 81 integers in
    the 1 to 9 interval (same row or column order than input), or None
    if no solution exists.
    '''
    try:
        i  = s.index(0)
    except ValueError: 
        # No empty cell left: solution found
        return s

    c = [s[j] for j in range(81)
         if not ((i-j)%9 * (i//9^j//9) * (i//27^j//27 | (i%9//3^j%9//3)))]

    for v in range(1, 10):
        if v not in c:
            r = solve(s[:i]+[v]+s[i+1:])
            if r is not None:
                return r

#-------------------------------------------------------------------------------
# Let's test it!
#
if __name__ == '__main__':
    class Sudoku(list):
        '''Sudokus with nicer IO'''
        def __init__(self, content):
            list.__init__(self, [int(i) for i in content.split()] 
                          if isinstance(content, str) else content)
        def __str__(self):
            return '\n'.join(
                ' '.join([(str(j) if j != 0 else '-') 
                          for j in self[i*9:(i+1)*9]]) for i in range(9))

    problem = Sudoku('''
        5 3 0 0 7 0 0 0 0
        6 0 0 1 9 5 0 0 0
        0 9 8 0 0 0 0 6 0
        8 0 0 0 6 0 0 0 3
        4 0 0 8 0 3 0 0 1
        7 0 0 0 2 0 0 0 6
        0 6 0 0 0 0 2 8 0
        0 0 0 4 1 9 0 0 5
        0 0 0 0 8 0 0 7 9
        ''')

    solution = Sudoku('''
        5 3 4 6 7 8 9 1 2
        6 7 2 1 9 5 3 4 8
        1 9 8 3 4 2 5 6 7
        8 5 9 7 6 1 4 2 3
        4 2 6 8 5 3 7 9 1
        7 1 3 9 2 4 8 5 6
        9 6 1 5 3 7 2 8 4
        2 8 7 4 1 9 6 3 5
        3 4 5 2 8 6 1 7 9
        ''')

    result = Sudoku(solve(problem))

    print('==== Problem ====\n{0}\n\n=== Solution ====\n{1}'.format(
            problem, result))
    
    assert(result == solution)
