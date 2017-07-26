def qsort(L):
    if len(L) <= 1: return L
    return qsort( [ lt for lt in L[1:] if lt < L[0] ] )  +  \ 
              [ L[0] ]  +  qsort( [ ge for ge in L[1:] if ge >= L[0] ] )


# IMHO this is almost as nice as the Haskell version from www.haskell.org:
# qsort [] = [] 
# qsort (x:xs) = qsort elts_lt_x ++ [x] ++ qsort elts_greq_x
#                 where 
#                   elts_lt_x = [y | y <- xs, y < x] 
#                   elts_greq_x = [y | y <- xs, y >= x]

# And here's a test function:
def qs_test(length):
    import random
    joe = range(length)
    random.shuffle(joe)
    qsJoe = qsort(joe)
    for i in range(len(qsJoe)):
        assert qsJoe[i] == i, 'qsort is broken!'
