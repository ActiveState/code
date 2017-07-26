def unzip(args):
    """
    inverse of zip. Given: ((1,"a"),(2,"b")) --> ((1,2),("a","b"))

    seq == unzip(zip(seq)) if seq is a rectangular matrix (all of its row has the same length.
    """
    result = []
    n = min(map(len,args))
    for i in range(n):result.append([])
    for i in range(len(args)):
        for j in range(n):
            result[j].append(args[i][j])
    return tuple(result)
