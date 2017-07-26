from itertools import islice
import constraint

def make_problem(blocks=9, block_size=3, possible_values=range(1, 10)):
    indices = list(range(i*blocks, i*blocks+blocks) for i in xrange(blocks))
    problem = constraint.Problem()

    def ensure_unique_values(varnames):
        # we don't want variable names to interfere with values,
        # so we convert them to strings
        problem.addConstraint(constraint.AllDifferentConstraint(), map(str, varnames))

    for vars in indices:
        problem.addVariables(map(str, vars), possible_values)
        # ensure all values are unique per row
        ensure_unique_values(vars)

    for vars in zip(*indices):
        # ensure all values are unique per column
        ensure_unique_values(vars)

    def block_indices(n):
        (x, y) = divmod(n, block_size)
        x *= block_size
        y *= block_size
        g_indices = list()
        for i in xrange(block_size):
            g_indices.extend(indices[x+i][y:y+block_size])
        return g_indices

    for i in xrange(blocks):
        # ensure all values are unique per block
        ensure_unique_values(block_indices(i))

    return problem

class Unsolvable(Exception):
    pass

def solve(matrix, problem=None):
    if problem is None:
        problem = make_problem()
    for (varn, val) in enumerate(sum(matrix, [])):
        if val is not None:
            problem.addConstraint(lambda var, val=val: var==int(val), variables=(str(varn),))

    soln = problem.getSolution()
    if soln is None:
        raise Unsolvable()

    # soln is a dictionary of indices to values
    values = (v for (k, v) in sorted(soln.iteritems(), key=lambda (k, v): int(k)))
    cols = len(matrix)

    while True:
        row = list(islice(values, cols))
        if not row:
            break
        yield row

# example

difficult = '''
X 4 X  X X X  X X X
X X X  X X 6  5 X 4
3 6 X  X 5 8  9 X X

9 8 X  X X X  X X X
X X X  5 7 2  X X X
X X X  X X X  X 4 1

X X 3  7 2 X  X 5 9
2 X 5  8 X X  X X X
X X X  X X X  X 3 X
'''

def text_puzzle_to_matrix(s, wildcard='X'):
    m = list()
    for line in s.split('\n'):
        if len(line) == 0:
            continue
        line = line.split()
        for (i, token) in enumerate(line):
            if token == wildcard:
                line[i] = None
        m.append(line)
    return m

for r in solve(text_puzzle_to_matrix(difficult)):
    print r
