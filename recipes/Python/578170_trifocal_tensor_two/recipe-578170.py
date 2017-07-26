def tensor(a,b):
    '''Returns the 3x3x3 (27 element) trifocal tensor given two 3x4 camera matrices.
    '''
    T = zeros((3,3,3))
    for i in range(3):
        T[i] = outer(a[:,i],b[:,3]) - outer(a[:,3],b[:,i])
    return T

# OR, given A and B 3x4 arrays

T = array([(outer(a[:,i],b[:,3]) - outer(a[:,3],b[:,i])) for i in range(3)])
