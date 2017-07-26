mod = lambda n,m: n%m
def baseExpansion(n,c,b):
    i = len(n)
    base10 = sum([pow(c,i-k-1)*n[k] for k in range(i)])
    j = int(ceil(log(base10 + 1,b)))
    baseExpanded = [mod(base10//pow(b,j-p),b) for p in range(1,j+1)]
    return baseExpanded
