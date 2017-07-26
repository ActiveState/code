def homogeneous(mylist, *types):
    '''
    >>> homogeneous([ 12, 3, 4, 4.33, 3.14, 'ola', 'string', [], None, [1, 3, 3], {}], int, type(None)) => [12, 3, 4, None]
    '''
    return [item for item in mylist if type(item) in types]      
