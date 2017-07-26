from random import uniform, sample

def order(x, NoneIsLast = True, decreasing = False):
    """
    Returns the ordering of the elements of x. The list
    [ x[j] for j in order(x) ] is a sorted version of x.

    Missing values in x are indicated by None. If NoneIsLast is true,
    then missing values are ordered to be at the end.
    Otherwise, they are ordered at the beginning.
    """
    omitNone = False
    if NoneIsLast == None:
        NoneIsLast = True
        omitNone = True
        
    n  = len(x)
    ix = range(n)
    if None not in x:
        ix.sort(reverse = decreasing, key = lambda j : x[j])
    else:
        # Handle None values properly.
        def key(i, x = x):
            elem = x[i]
            # Valid values are True or False only.
            if decreasing == NoneIsLast:
                return not(elem is None), elem
            else:
                return elem is None, elem
        ix = range(n)
        ix.sort(key=key, reverse=decreasing)
            
    if omitNone:
        n = len(x)
        for i in range(n-1, -1, -1):
            if x[ix[i]] == None:
                n -= 1
        return ix[:n]
    return ix


def rank(x, NoneIsLast=True, decreasing = False, ties = "first"):
    """
    Returns the ranking of the elements of x. The position of the first
    element in the original vector is rank[0] in the sorted vector.

    Missing values are indicated by None.  Calls the order() function.
    Ties are NOT averaged by default. Choices are:
         "first" "average" "min" "max" "random" "average"
    """
    omitNone = False
    if NoneIsLast == None:
        NoneIsLast = True
        omitNone = True
    O = order(x, NoneIsLast = NoneIsLast, decreasing = decreasing)
    R = O[:]
    n = len(O)
    for i in range(n):
        R[O[i]] = i
    if ties == "first" or ties not in ["first", "average", "min", "max", "random"]:
        return R
        
    blocks     = []
    isnewblock = True
    newblock   = []
    for i in range(1,n) :
        if x[O[i]] == x[O[i-1]]:
            if i-1 not in newblock:
                newblock.append(i-1)
            newblock.append(i)
        else:
            if len(newblock) > 0:
                blocks.append(newblock)
                newblock = []
    if len(newblock) > 0:
        blocks.append(newblock)

    for i, block  in enumerate(blocks):
        # Don't process blocks of None values.
        if x[O[block[0]]] == None:
            continue
        if ties == "average":
            s = 0.0
            for j in block:
                s += j
            s /= float(len(block))
            for j in block:
                R[O[j]] = s                
        elif ties == "min":
            s = min(block)
            for j in block:
                R[O[j]] = s                
        elif ties == "max":
            s =max(block)
            for j in block:
                R[O[j]] = s                
        elif ties == "random":
            s = sample([O[i] for i in block], len(block))
            for i,j in enumerate(block):
                R[O[j]] = s[i]
        else:
            for i,j in enumerate(block):
                R[O[j]] = j
    if omitNone:
        R = [ R[j] for j in range(n) if x[j] != None]
    return R

if __name__ == "__main__":
    """
    Output when run from the command line:

vector  [5, None, None, 6, 2, 3, 2, 0, 5, 5, 1, None]
order(NoneIsLast= True ,decreasing= True ) [3, 0, 8, 9, 5, 4, 6, 10, 7, 1, 2, 11]
rank(x, NoneIsLast= True ,decreasing= True ,ties= first ) [1, 9, 10, 0, 5, 4, 6, 8, 2, 3, 7, 11]
rank(x, NoneIsLast= True ,decreasing= True ,ties= average ) [2.0, 9, 10, 0, 5.5, 4, 5.5, 8, 2.0, 2.0, 7, 11]
rank(x, NoneIsLast= True ,decreasing= True ,ties= min ) [1, 9, 10, 0, 5, 4, 5, 8, 1, 1, 7, 11]
rank(x, NoneIsLast= True ,decreasing= True ,ties= max ) [3, 9, 10, 0, 6, 4, 6, 8, 3, 3, 7, 11]
rank(x, NoneIsLast= True ,decreasing= True ,ties= random ) [0, 9, 10, 0, 6, 4, 4, 8, 9, 8, 7, 11]

order(NoneIsLast= True ,decreasing= False ) [7, 10, 4, 6, 5, 0, 8, 9, 3, 1, 2, 11]
rank(x, NoneIsLast= True ,decreasing= False ,ties= first ) [5, 9, 10, 8, 2, 4, 3, 0, 6, 7, 1, 11]
rank(x, NoneIsLast= True ,decreasing= False ,ties= average ) [6.0, 9, 10, 8, 2.5, 4, 2.5, 0, 6.0, 6.0, 1, 11]
rank(x, NoneIsLast= True ,decreasing= False ,ties= min ) [5, 9, 10, 8, 2, 4, 2, 0, 5, 5, 1, 11]
rank(x, NoneIsLast= True ,decreasing= False ,ties= max ) [7, 9, 10, 8, 3, 4, 3, 0, 7, 7, 1, 11]
rank(x, NoneIsLast= True ,decreasing= False ,ties= random ) [0, 9, 10, 8, 6, 4, 4, 0, 8, 9, 1, 11]


order(NoneIsLast= False ,decreasing= True ) [1, 2, 11, 3, 0, 8, 9, 5, 4, 6, 10, 7]
rank(x, NoneIsLast= False ,decreasing= True ,ties= first ) [4, 0, 1, 3, 8, 7, 9, 11, 5, 6, 10, 2]
rank(x, NoneIsLast= False ,decreasing= True ,ties= average ) [5.0, 0, 1, 3, 8.5, 7, 8.5, 11, 5.0, 5.0, 10, 2]
rank(x, NoneIsLast= False ,decreasing= True ,ties= min ) [4, 0, 1, 3, 8, 7, 8, 11, 4, 4, 10, 2]
rank(x, NoneIsLast= False ,decreasing= True ,ties= max ) [6, 0, 1, 3, 9, 7, 9, 11, 6, 6, 10, 2]
rank(x, NoneIsLast= False ,decreasing= True ,ties= random ) [9, 0, 1, 3, 6, 7, 4, 11, 0, 8, 10, 2]

order(NoneIsLast= False ,decreasing= False ) [1, 2, 11, 7, 10, 4, 6, 5, 0, 8, 9, 3]
rank(x, NoneIsLast= False ,decreasing= False ,ties= first ) [8, 0, 1, 11, 5, 7, 6, 3, 9, 10, 4, 2]
rank(x, NoneIsLast= False ,decreasing= False ,ties= average ) [9.0, 0, 1, 11, 5.5, 7, 5.5, 3, 9.0, 9.0, 4, 2]
rank(x, NoneIsLast= False ,decreasing= False ,ties= min ) [8, 0, 1, 11, 5, 7, 5, 3, 8, 8, 4, 2]
rank(x, NoneIsLast= False ,decreasing= False ,ties= max ) [10, 0, 1, 11, 6, 7, 6, 3, 10, 10, 4, 2]
rank(x, NoneIsLast= False ,decreasing= False ,ties= random ) [9, 0, 1, 11, 4, 7, 6, 3, 0, 8, 4, 2]


order(NoneIsLast= None ,decreasing= True ) [3, 0, 8, 9, 5, 4, 6, 10, 7]
rank(x, NoneIsLast= None ,decreasing= True ,ties= first ) [1, 9, 10, 0, 5, 4, 6, 8, 2, 3, 7, 11]
rank(x, NoneIsLast= None ,decreasing= True ,ties= average ) [2.0, 0, 5.5, 4, 5.5, 8, 2.0, 2.0, 7]
rank(x, NoneIsLast= None ,decreasing= True ,ties= min ) [1, 0, 5, 4, 5, 8, 1, 1, 7]
rank(x, NoneIsLast= None ,decreasing= True ,ties= max ) [3, 0, 6, 4, 6, 8, 3, 3, 7]
rank(x, NoneIsLast= None ,decreasing= True ,ties= random ) [9, 0, 6, 4, 4, 8, 8, 0, 7]

order(NoneIsLast= None ,decreasing= False ) [7, 10, 4, 6, 5, 0, 8, 9, 3]
rank(x, NoneIsLast= None ,decreasing= False ,ties= first ) [5, 9, 10, 8, 2, 4, 3, 0, 6, 7, 1, 11]
rank(x, NoneIsLast= None ,decreasing= False ,ties= average ) [6.0, 8, 2.5, 4, 2.5, 0, 6.0, 6.0, 1]
rank(x, NoneIsLast= None ,decreasing= False ,ties= min ) [5, 8, 2, 4, 2, 0, 5, 5, 1]
rank(x, NoneIsLast= None ,decreasing= False ,ties= max ) [7, 8, 3, 4, 3, 0, 7, 7, 1]
rank(x, NoneIsLast= None ,decreasing= False ,ties= random ) [9, 8, 4, 4, 6, 0, 0, 8, 1]
    """
    x = [5, None, None, 6, 2, 3, 2, 0, 5, 5, 1, None]
    print "vector ", x
    for NoneIsLast in [True, False, None]:
        for decreasing in [True, False]:
            O = order(x, NoneIsLast=NoneIsLast, decreasing=decreasing)
            print "order(NoneIsLast=", NoneIsLast, ",decreasing=", decreasing, ")", O

            for ties in ["first", "average", "min", "max", "random"]:
                R = rank(x, NoneIsLast=NoneIsLast, decreasing=decreasing, ties=ties)
                print "rank(x, NoneIsLast=", NoneIsLast, ",decreasing=", decreasing, ",ties=", ties, ")", R
            print
        print
