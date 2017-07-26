def eratosthenes(n):
    N=range(n+1)
    z=[0]*(n/2)
    for i in range(2, int(n**.5)+1):
        if N[i]:
            N[i*i::i] = z[:(n/i)-i+1]
    return filter(None, N[2:])
