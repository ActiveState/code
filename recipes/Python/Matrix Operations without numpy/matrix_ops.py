def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def multip(X, Y):
    return [[sum(a*b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]


def getMatrixMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]


def getMatrixDeternminant(m):
    # base case for 2x2 matrix
    if len(m) == 2:
        return (m[0][0]*m[1][1]-m[0][1]*m[1][0])*1.0

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1.0)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m, 0, c))
    return determinant


def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    # find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors