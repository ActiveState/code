import random
def tcnfgen(m,k,horn=1):
    cnf = []
    def unique(l,k):
        t = random.randint(1,k)
        while(t in l):
            t = random.randint(1,k)
        return t
    r = (lambda : random.randint(0,1))
    for i in range(m):
        x = unique([],k)
        y = unique([x],k)
        z = unique([x, y],k)
        if horn:
            cnf.append([(x,1), (y,0),(z,0)])
        else:
            cnf.append([(x,r()), (y,r()),(z,r())])
    return cnf
