def deepFlatten(lista):
    '''
    >>> list(deepFlatten([1,2,[], [1], 3, [4, [5,6]], 7, 'oi', None])) => [1, 2, 1, 3, 4, 5, 6, 7, 'o', 'i', None]
    '''
    try:
        for item in lista:
            for one in deepFlatten(item):
                yield one
    except:
        yield lista
