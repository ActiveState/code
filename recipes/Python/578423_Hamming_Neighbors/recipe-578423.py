def HammingNeighbors(n, dist, numBits):
    """Returns list of numbers that are given hamming distance away                                                                        
    from an integer.                                                                                                                       
                                                                                                                                           
    n : an integer                                                                                                             
    dist : Hamming distance                                                                                                                
    bits : number of bits of neighbors                                                                                                     
    """
    if dist < 0:
        raise Exception, 'Invalid distance'
    onesMask = int('1'*numBits, 2)

    # Cur array maintains the invariant that for some dist d,                                                                                  
    # Cur[i] holds all numbers that that are d distance                                                                                    
    # away from lower i-bits of n                                                                                                          

    # dist == 0                                                                                                                            
    Cur = [[n % (1 <<  _)] for _ in range(numBits+1)]
    # dist > 0
    for d in range(1, dist+1):
        Prev = Cur
        Cur = [[] for _ in range(numBits+1)]
        for i in range(d, numBits+1):
            # n's i-th bit and its inversion                                                                                               
            iBit = n & (1<<i-1)
            iBitInv = iBit ^ (1<<i-1)
            Cur[i] = [iBitInv + x for x in Prev[i-1]] + \
                     [iBit + x for x in Cur[i-1]]
    return Cur[numBits]
