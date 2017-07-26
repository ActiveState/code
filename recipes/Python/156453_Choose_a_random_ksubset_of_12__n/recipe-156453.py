from random import random, randrange

def ranksb ( N, K ) :
    if N < K :
        raise Exception, "N must be no less than K"
    if K == 0 : return [ ]

    L2 = K + 1
    R = L2
    A = K * [ 0 ]
    while 1 :
        M = 1 + int ( random ( ) * N )
        I = 1 + ( M - 1 ) % K
        breakthencontinue = 0
        if A [ I - 1 ]  != 0 :
            while M != A [ I - 1 ] / L2 :
                LINK = A [ I - 1 ] % L2
                if LINK == 0 :
                    while 1 :
                        R -= 1
                        if R == 0 : return map ( lambda a : a / L2, A )
                        if A [ R - 1 ] <= 0 :
                            A [ I - 1 ]  += R
                            I = R
                            A [ I - 1 ] = L2 * M
                            break
                    breakthencontinue = 1
                    break
                I = LINK
            else :
                continue
        if breakthencontinue :
            continue
        A [ I - 1 ] = L2 * M

if __name__ == "__main__" :
    from fpformat import fix
    from time import time

    counts = { }
    n , k = 105, 90
    sampleSize = 1000

    timeStart = time ( )
    for s in xrange ( sampleSize ) :
        a = ranksb ( n, k )
        for i in a :
            if i in counts :
                counts [ i ] += 1
            else :
                counts [ i ] = 1
    print "Time to generate %i %i-subsets from set of size %i: %s seconds" \
        % ( sampleSize, k, n, fix ( time ( ) - timeStart, 3 ) )

    keys = counts . keys ( )
    keys . sort ( )
    totalCount = 0
    idealCount = sampleSize * k / n
    ChiSquare = 0
    print "Counts of occurrences of each sample element, "
    print "and difference between 'ideal' count and actual"
    for key in keys :
        print key, counts [ key ], abs ( counts [ key ] - idealCount )
        totalCount += counts [ key ]
        ChiSquare +=float ( pow ( counts [ key ] - idealCount, 2 ) ) / idealCount
    print "Chi-squared test of uniformity: %s on %i d.f." % ( fix ( ChiSquare, 3), n - 1 )
