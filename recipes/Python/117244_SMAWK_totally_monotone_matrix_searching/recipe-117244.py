# SMAWK totally monotone matrix searching algorithm
# David Eppstein, UC Irvine, 17 Mar 2002

# reference:
# A. Aggarwal, M. Klawe, S. Moran, P. Shor and R. Wilber,
# Geometric applications of a matrix searching algorithm,
# Algorithmica 2, pp. 195-208 (1987).

def smawk(rows,cols,lookup):
    '''Search for row-maxima in a 2d totally monotone matrix M[i,j].
    The input is specified by a list of row indices, a list of column
    indices, and a function "lookup" satisfying lookup(i,j) = M[i,j].
    The matrix must satisfy the totally monotone ordering property:
    if i occurs before i' in rows, j occurs before j' in cols, and
    M[i,j] < M[i,j'], then also M[i',j] < M[i',j'].  The result is
    returned as a dictionary mapping row i to the column j containing
    the largest value M[i,j].  Ties are broken in favor of earlier
    columns.  The number of calls to lookup is O(len(rows)+len(cols)).'''
	
    # base case of recursion
    if not rows: return {}
	
    # reduce phase: make number of columns at most equal to number of rows
    stack = []
    for c in cols:
        while len(stack) >= 1 and \
          lookup(rows[len(stack)-1],stack[-1]) < lookup(rows[len(stack)-1],c):
            stack.pop()
        if len(stack) != len(rows):
            stack.append(c)

    cols = stack

    # recursive call to search for every odd row
    result = smawk([rows[i] for i in xrange(1,len(rows),2)],cols,lookup)

    # go back and fill in the even rows
    c = 0
    for r in xrange(0,len(rows),2):
        row = rows[r]
        if r == len(rows) - 1:
            cc = len(cols)-1  # if r is last row, search through last col
        else:
            cc = c            # otherwise only until pos of max in row r+1
            target = result[rows[r+1]]
            while cols[cc] != target:
                cc += 1
        result[row] = max([ (lookup(row,cols[x]),-x,cols[x]) \
                            for x in xrange(c,cc+1) ]) [2]
        c = cc

    return result


# Example application: All nearest neighbors of points on a line
# Exercise: verify that negDist satisfies the totally monotone matrix property.

def linearNearestNeighbors(A,B):
    '''Takes as input a set of points A and B in some Euclidean space.
    A lies on the x-axis and is given as a sequence of real numbers;
    B is given in Cartesian coordinates (tuples of real numbers).
    Output is a dict mapping each point in A to the nearest point in B.'''

    # negate squared Euclidean distance to convert minimization of distance
    # into a maximization problem suitable for SMAWK algorithm
    def square(x): return x*x
    def negDist(a,b):
        dist = square(b[0]-a)
        for i in range(1,len(b)):
            dist += square(b[i])
        return -dist
	
    A.sort()	# make sure points are sorted, omit if already sorted
    B.sort()
    return smawk(A,B,negDist)
