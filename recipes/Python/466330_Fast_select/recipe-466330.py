def select(pos, seq):
    """select(pos, seq): find the nth rank ordered element
    (the least value has rank 0).
    Note1: it modifies the seq.
    Note2: this function is useful with Psyco, otherwise .sort is
    faster until len(seq)>~3e6"""
    # Version 1.1, Nov 13 2004, from "Numerical Recipes".
    lo = 0
    up = len(seq)-1
    if pos<lo or pos>up:
        raise 'Selection out of bounds.'
    else:
        while up>=pos and pos>=lo:
            i = lo
            j = up
            tempr = seq[pos]
            seq[pos] = seq[lo]
            seq[lo] = tempr
            # Split in two
            while i<j:
                while seq[j] > tempr:
                    j -= 1
                seq[i] = seq[j]
                while i<j and seq[i]<=tempr:
                    i += 1
                seq[j] = seq[i]
            seq[i] = tempr
            # Select sub
            if pos<i:
                up = i-1
            else:
                lo = i+1
        return seq[pos]


try: # Import Psyco if available.
# Psyco is almost necessary, otherwise .sort is faster until len(seq)>~3e6
    import psyco
except ImportError:
    pass
else:
    psyco.bind(select)


if __name__ == '__main__': # Test ----------------------
    from time import clock
    import random
    nrepetiotions = 6
    print "nrepetiotions=", nrepetiotions
    print "len(list), average min time select of 1"\
          "element of list, min time select(list):"
    for j in xrange(6, 21):
        n = 2**j
        v = []
        for i in range(nrepetiotions):
            seq = [random.random() for x in xrange(n+1)]
            nd2 = int(n//2)
            t1 = clock()
            select(nd2, seq)
            t2 = clock()
            v.append(t2-t1)
        print "2^"+str(j)+"=", n, round(1000000*min(v)/n, 3), round(min(v), 3)
