def comb(*sequences):
    '''
    combinations of multiple sequences so you don't have
    to write nested for loops
    
    >>> from pprint import pprint as pp
    >>> pp(comb(['Guido','Larry'], ['knows','loves'], ['Phyton','Purl']))
    [['Guido', 'knows', 'Phyton'],
     ['Guido', 'knows', 'Purl'],
     ['Guido', 'loves', 'Phyton'],
     ['Guido', 'loves', 'Purl'],
     ['Larry', 'knows', 'Phyton'],
     ['Larry', 'knows', 'Purl'],
     ['Larry', 'loves', 'Phyton'],
     ['Larry', 'loves', 'Purl']]
    >>> 
    '''
    combinations = [[seq] for seq in sequences[0]]
    for seq in sequences[1:]:
        combinations = [comb+[item]
                        for comb in combinations
                        for item in seq ]
    return combinations

def comb2(*sequences):
    '''
    Generator of combinations of multiple sequences so you don't have
    to write nested for loops

    Note: rightmost sequence changes the quickest as if it were the inner loop.    
    
    >>> for x in comb2(['Guido','Larry'], ['knows','loves','hates'], ['Phyton','Purl','Wuby','Auk']):
    ... 	print x
    ... 	
    ['Guido', 'knows', 'Phyton']
    ['Guido', 'knows', 'Purl']
    ['Guido', 'knows', 'Wuby']
    ['Guido', 'knows', 'Auk']
    ['Guido', 'loves', 'Phyton']
    ['Guido', 'loves', 'Purl']
    ['Guido', 'loves', 'Wuby']
    ['Guido', 'loves', 'Auk']
    ['Guido', 'hates', 'Phyton']
    ['Guido', 'hates', 'Purl']
    ['Guido', 'hates', 'Wuby']
    ['Guido', 'hates', 'Auk']
    ['Larry', 'knows', 'Phyton']
    ['Larry', 'knows', 'Purl']
    ['Larry', 'knows', 'Wuby']
    ['Larry', 'knows', 'Auk']
    ['Larry', 'loves', 'Phyton']
    ['Larry', 'loves', 'Purl']
    ['Larry', 'loves', 'Wuby']
    ['Larry', 'loves', 'Auk']
    ['Larry', 'hates', 'Phyton']
    ['Larry', 'hates', 'Purl']
    ['Larry', 'hates', 'Wuby']
    ['Larry', 'hates', 'Auk']
    >>>

    The algorithm relies on noting the following and generalising:

    If you had three sequences of length 2, 3, and 4 left-to-right,
    Then the indices of the *elements* for all combinations can be
    generated with:
        for x in range(2*3*4): 
            print ( (x/(3*4*1))%2, (x/(4*1))%3, (x/(1))%4 )
    
    '''
    import operator
    
    lengths = [len(seq) for seq in sequences]
    range_len_seq = range(len(sequences))
    max_count = reduce(operator.mul, lengths)
    _tmp = lengths + [1]        # append multiplicative identity
    dividers = [reduce(operator.mul, _tmp[-x-1:]) for x in range_len_seq][::-1]
    modulos = lengths
    for n in range(max_count):
        yield [sequences[r][(n/dividers[r])%modulos[r]] for r in range_len_seq]
