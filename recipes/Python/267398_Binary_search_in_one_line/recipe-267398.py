def search(n, L):
    f = lambda n,L,o: len(L) and ( \
        (n == L[len(L)/2])*(len(L)/2+o) or \
        (n < L[len(L)/2] and f(n,L[:len(L)/2],o)) or \
        (n > L[len(L)/2] and f(n,L[len(L)/2+1:],o+len(L)/2+1)))

    return f(n,L,1) - 1
