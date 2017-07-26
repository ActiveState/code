def  splice(alists, recycle = True):
    """
    Accepts a list of nonempty lists or indexable objects in
    argument alists (each element list may not be of the same
    length) and a keyword argument recycle which
    if true will reuse elements in lists of shorter length.

    Any error will result in an empty list to be returned.
    """

    try:
        nlists = len(alists)
        lens   = [len(alist) for alist in alists]
        if not recycle:
            totlen = sum(lens)
        else:
            totlen = max(lens) * nlists
            
        pos  = [0] * nlists
        R    = [None] * totlen
        i, j = 0, 0
        while i < totlen:
            if pos[j] < lens[j]:
                R[i]     = alists[j][pos[j]]
                i        += 1
                pos[j] = pos[j] + 1
                if recycle and pos[j] >= lens[j]:
                    pos[j] = 0
            j = (j + 1) % nlists
        return R
    except:
        return []

if __name__ == "__main__":
    print splice([[1,2,3], ['a','b'], [4], [-1,-2,-3,-4]], recycle = False)
    print splice([[1,2,3], ['a','b'], [4], [-1,-2,-3,-4]])

    
        
        
    
