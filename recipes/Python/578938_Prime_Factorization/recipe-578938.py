def primo(n):
    def z(x):
        if x % i : return True
        if x == i: return True
        return False
    nump =[2]+ range(3, n+1, 2) 
    for i in range(3, int((n**0.5)+1),2): 
        nump = filter(z, nump)
    return nump

def mcm(n):
    p=primo(n); mm=[]
    while(n > 1):
        for i in p:
            if (n%i == 0): mm.append(i); n=n/i
    mm.sort()
    return mm                


for k in range(100,121):
    print k," ",mcm(k)
