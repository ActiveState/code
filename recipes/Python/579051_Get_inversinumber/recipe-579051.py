def inversion(permList):
    """
    Description - This function returns the number of inversions in a
                  permutation.
    Preconditions - The parameter permList is a list of unique positve numbers.

    Postconditions - The number of inversions in permList has been returned.

    Input - permList : list
    Output - numInversions : int
    """
    if len(permList)==1:
        return 0
    else:
        numInversion=len(permList)-permList.index(max(permList))-1
        permList.remove(max(permList))
        return numInversion+inversion(permList)
