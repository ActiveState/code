#!/usr/bin/env python

__version__ = "0.8"

"""xcombinations.py

This recipe shows a way to solve the K-combination problems without replacement
of a N items sequence using the dynamic programming technique.

Keywords: combination, binomial coefficient, generator

See also: http://code.activestate.com/recipes/577764-combinations-of-a-sequence-without-replacement-usi/
See also: http://code.activestate.com/recipes/190465-generator-for-permutations-combinations-selections/ 
See also: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/105962
See also: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66463
See also: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66465

"""



def xcombinations(s, K):
    """
    On entry: s sequence of items; K size of the combinations
    Returns: generator of the K-combinations without replacement of
    s.
    """
    N = len(s)
    assert K<=N, 'Error K must be less or igual than N'
    S = [[] for i in range(K) ]
    for n in range(1,N+1):
        newS = [[] for i in range(K) ]
        for k in range(max(1, n-(N-K)), min(K+1, n+1)):
            if k == K:
                for el in S[k-1]:
                    yield el+[s[n-1]] 
            else:
                newS[k].extend(S[k])
                if len(S[k-1])==0:
                    newS[k].append([s[n-1]])
                else:
                    newS[k].extend( [el+[s[n-1]] for el in S[k-1]] )
        S = newS



if __name__ == '__main__':

    s = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    for c in xcombinations(s, 5):
        print c
