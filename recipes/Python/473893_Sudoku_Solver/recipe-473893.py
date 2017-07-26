n = 3       # Size of inner region
n2, n3, n4 = n**2, n**3, n**4

def show(flatline):
    'Display grid from a string (values in row major order with blanks for unknowns)'
    fmt = '|'.join(['%s' * n] * n)
    sep = '+'.join(['-'  * n] * n)
    for i in range(n):
        for j in range(n):
            offset = (i*n+j)*n2
            print fmt % tuple(flatline[offset:offset+n2])
        if i != n-1:
            print sep

def _find_friends(cell):
    'Return tuple of cells in same row, column, or subgroup'
    friends = set()
    row, col = cell // n2, cell % n2
    friends.update(row * n2 + i for i in range(n2))
    friends.update(i * n2 + col for i in range(n2))   
    nw_corner = row // n * n3 + col // n * n
    friends.update(nw_corner + i + j for i in range(n) for j in range(0,n3,n2))
    friends.remove(cell)
    return tuple(friends)
friend_cells = map(_find_friends, range(n4))

def select_an_unsolved_cell(possibles, heuristic=min):
    # Default heuristic:  select cell with fewest possibilities
    # Other possible heuristics include:  random.choice() and max()
    return heuristic((len(p), cell) for cell, p in enumerate(possibles) if len(p)>1)[1]

def solve(possibles, pending_marks):
    # Apply pending_marks (list of cell,value pairs) to possibles (list of str).
    # Mutates both inputs.  Return solution as a flat string (values in row-major order)
    # or return None for dead-ends where all possibilites have been eliminated.
    for cell, v in pending_marks:
        possibles[cell] = v
        for f in friend_cells[cell]:
            p = possibles[f]
            if v in p:
                p = possibles[f] = p.replace(v, '')     # exclude value v from friend f
                if not p:
                    return None               # Dead-end:  all possibilities eliminated
                if len(p) == 1:
                    pending_marks.append((f, p[0]))

    # Check to see if the puzzle is fully solved (each cell has only one possible value)
    if max(map(len, possibles)) == 1:
        return ''.join(possibles)
    
    # If it gets here, there are still unsolved cells
    cell = select_an_unsolved_cell(possibles)
    for v in possibles[cell]:           # try all possible values for that cell
        ans = solve(possibles[:], [(cell, v)])
        if ans is not None:
            return ans

# ----- Examples -----
for given in [
    '53  7    6  195    98    6 8   6   34  8 3  17   2   6 6    28    419  5    8  79',
    '       75  4  5   8 17 6   36  2 7 1   5 1   1 5 8  96   1 82 3   4  9  48       ',
    ' 9 7 4  1    6 2 8    1 43  6     59   1 3   97     8  52 7    6 8 4    7  5 8 2 ',
    '67 38      921   85    736 1 8  4 7  5 1 8 4  2 6  8 5 175    24   321      61 84',
    '27  15  8   3  7 4    7     5 1   7   9   2   6   2 5     8    6 5  4   8  59  41',
    ]:
    show(given)
    pending_marks = [(i,v) for i, v in enumerate(given) if v != ' ']
    possibles = ['123456789'] * len(given)
    result = solve(possibles, pending_marks)
    print
    show(result)
    print '=-' * 20
