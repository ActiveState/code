    '''
        Level 8 palindrome solution.
    
        Re: LEVEL 8
        by KannanKV on Wed Jan 13, 2010 11:17 pm
    
        hi lambertdw , you can post it after the contest is over at
        Jan 16, [2010] 9:00 P.M I.S.T ... Thank you for your patience !!
    
        Consider pairs.
    '''
    
    data = 'abccdadba'                      # test phrase has 50 palindromes.
    
    pairs = [(i,j,)for(i,a,)in enumerate(data)
             for j in range(i+1,len(data))if a==data[j]]
    
    intermediates = [j-i-1 for (i,j,) in pairs]
    
    # table[row][col] is True iff [pair number row] surrounds [pair number col]
    table = [[0,]*len(pairs)for pair in pairs]
    for (I,(i,l,),) in enumerate(pairs):
        for (J,(j,k,),) in enumerate(pairs):
            table[I][J] = (i < j) and (k < l)
    
    
    # all pairs occur once.  I chose to treat the zero pair separately.
    # another approach would be to surround the entire data string by
    # a sentinel character, such as space " "
    occurrences = [1 for pair in pairs]     # occurrences of pairs
    
    
    # recursive memo-ized function modifies global pair occurrences count.
    def f(k,d={},):
        if k in d:                          # may be faster with try/except
            L = d[k]
            for i in range(len(pairs)):     # loop can be shortened with more logic
                occurrences[i] += L[i]      # since we need start from k+1
            return
        enclosed = table[k]
        L = occurrences[:]
        for j in range(k+1,len(pairs)):
            if enclosed[j]:
                occurrences[j] += 1
                f(j)
        d[k] = [new-old for (new,old,) in zip(occurrences,L)]
    
    for k in range(len(pairs)):             # account for even palindromes from
        f(k)                                # all pairs.
    
    evens = sum(occurrences)
    odds = (
        len(data)
        +sum(occurrence*intermediate
             for (occurrence,intermediate,) in zip(occurrences,intermediates,)))
    
    print('Palindromes:',evens+odds)
