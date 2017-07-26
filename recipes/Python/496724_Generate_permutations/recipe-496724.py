def genbags(P,L = []):
    if not max(P):
        yield L
    else:
        for i,x in enumerate(P):
            if x: 
                P[i] -= 1
                for b in genbags(P,L+[i]): 
                    yield b
                P[i] += 1                

def histogram(seq):
    L = []
    R = []
    for i,x in enumerate(seq):
        try:
            R[L.index(x)] += 1
        except ValueError:
            R.append(1)
            L.append(x)
    return L,R

def perm(seq):
    L,R = histogram(seq)
    for Z in genbags(R):
        yield [L[i] for i in Z]
    
def test():
    P = [1],[1],[2],[3]
    for b in perm(P): 
        print b

if __name__=='__main__':
    test()
