from itertools import permutations

def tuples_sum(nbval,total,order=True) :
    """ 
        Generate all the tuples L of nbval positive or nul integer 
        such that sum(L)=total.
        The tuples may be ordered (decreasing order) or not
    """
    if nbval == 0 and total == 0 : yield tuple() ; raise StopIteration
    if nbval == 1 : yield (total,) ; raise StopIteration
    if total==0 : yield (0,)*nbval ; raise StopIteration
    for start in range(total,0,-1) :
        for qu in tuples_sum(nbval-1,total-start) :
            if qu[0]<=start :
                sol=(start,)+qu
                if order : yield sol
                else :
                    l=set()
                    for p in permutations(sol,len(sol)) :
                        if p not in l :
                            l.add(p)
                            yield p
    
if __name__=='__main__' :
    print("How to obtain 5 by adding a+b+c (>=0) ? ")
    print("Give me the list of (a,b,c) tuples.")
    g=tuples_sum(3,5,order=False)
    print(list(g))
    
    print("How to obtain 6 by adding 3 positive or nul integers ?")
    g=tuples_sum(3,6,order=True)
    print(list(g))
