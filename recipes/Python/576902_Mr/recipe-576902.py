from __future__ import division

from time import clock

from gmpy import *
from pysymbolicext import *
import psyco
psyco.full()

__all__=["carmichael","carmichael1","carmichael2","carmichael3","iscarmichael","clambda"]

#Carmichael numbers are odd composites C with at least 3 prime
#factors p(n) such that for each p(n) of C, p(n)-1 divides C-1

def carmichael1(a,b,limit=1000):
    """
    carmichael(a,b)
    For a,b (odd primes) returns array of c
    such that a*b*c is a Carmichael number
    """
    if a==b or a==2 or b==2: return []
    if not is_prime(a) or not is_prime(b): return []
    ab=a*b
    l=lcm(a-1,b-1)
    m1=ab%l
    m2=invert(m1,l)
    abl=ab*l
    c=m2
    while c<=max(a,b):
        c+=l
    xm1=ab*c-1
    solutions=[]
    while c<=limit:
        if (xm1)%(c-1)==0 and is_prime(c):
            solutions.append(c)
        c+=l
        xm1+=abl
    return solutions

def carmichael2(a,b,limit=1000):
    """
    carmichael(a,b)
    For a,b (odd primes) returns array of c
    such that a*b*c is a Carmichael number
    """
    if a==b or a==2 or b==2: return []
    if not is_prime(a) or not is_prime(b): return []
    am1=a-1
    bm1=b-1
    am1bm1=am1*bm1
    g,s,t=gcdext(am1bm1,-(am1+b))
    c=((t*(am1+bm1)//g))%bm1+1
    while c<=max(a,b):
        c+=bm1
    xm1=(a)*(b)*(c)-1
    inc=a*b*bm1
    solutions=[]
    while c<=limit:
        if (xm1)%(c-1)==0 and is_prime(c):
            solutions.append(c)
        c+=bm1
        xm1+=inc
    return solutions

#A different approach,but seems slower on many inputs
def carmichael3(*args):
    """
    carmichael(*args)  (last arg is search limit)
    For p1...pn (odd distinct primes) returns array of c
    such that p1*p2...pn*c is a Carmichael number.
    """
    limit=args[-1]
    args=args[:-1]
    if 2 in args: return []

    for arg in args:
        if not is_prime(arg): return []
    product=reduce(lambda a,b : a*b, args)
    l=reduce(lambda a,b : lcm(a,b), (x-1 for x in args))
    m1=product%l
    m2=invert(m1,l)
    productl=product*l
    c=m2
    while c<=max(args):
        c+=l
    xm1=product*c-1
    solutions=[]
    while c<=limit:
        if (xm1)%(c-1)==0 and is_prime(c):
            solutions.append(c)
        c+=l
        xm1+=productl
    return solutions

def carmichael(*args):
    """
    carmichael(*args)  (last arg is search limit)
    For p1...pn (odd distinct primes) returns array of c
    such that p1*p2...pn*c is a Carmichael number.
    Redirection function - calls carmichael 1 or 2
    depending on number of arguments.
    """
    if len(args)==3:
        return carmichael1(*args)
    else:
        return carmichael3(*args)

def iscarmichael(*args):
    """
    iscarmichael(*args). args are prime factors.
    Naively tests if the product of the given factors
    is a Carmichael number
    """
    for arg in args:
        if not is_prime(arg):
            return False
    xm1=reduce(lambda a,b : a*b, args)-1
    for arg in args:
        if xm1%(arg-1)!=0:
            return False
    return True

def cgenerate(limit=1000000,a=6,b=12,c=18):
    """
    cgenerate(a,b,c,limit)
    Return a list of all Carmichael numbers of the
    form (ak+1)*(bk+1)*(ck+1) up to limit
    """
    print "Using search limit",limit
    result=[]
    k=1
    while True:
        a1=a*k+1
        b1=b*k+1
        c1=c*k+1
        n=a1*b1*c1
        if n>limit:
            break
        if is_prime(a1) and is_prime(b1) and is_prime(c1):
            result.append((a1,b1,c1,n))
            #result.append(n)
        k+=1
    return result

def clambda(n):
    """
    clambda(n)
    Returns Carmichael's lambda function for positive integer n.
    Relies on factoring n
    """
    smallvalues=[1,1,2,2,4,2,6,2,6,4,10,2,12,6,4,4,16,6,18,4,6,10,22,2,20,12,18,\
    6,28,4,30,8,10,16,12,6,36,18,12,4,40,6,42,10,12,22,46,4,42,20,16,12,52,18,\
    20,6,18,28,58,4,60,30,6,16,12,10,66,16,22,12,70,6,72,36,20,18,30,12,78,4,54,\
    40,82,6,16,42,28,10,88,12,12,22,30,46,36,8,96,42,30,20]

    if n<=100: return smallvalues[n-1]
    factors=factor(n)
    l1=[]
    for p,e in factors:
        if p==2 and e>2:
            l1.append(2**(e-2))
        else:
            l1.append((p-1)*p**(e-1))
    return reduce(lambda a,b : lcm(a,b), l1)

numbers=cgenerate(100000000000000000000,2,4,14)
for x in numbers:
   print x[3],
   if iscarmichael(x[0],x[1],x[2]):
       print "is a Carmichael number"
   else:
       print

#----------------------------------TEST  CODE----------------------------------#

if __name__=="__main__":

    def naive(a,b,limit):
        """
        naive(a,b,limit).
        Naive implementation for benchmarking comparison.
        """
        if a==b or a==2 or b==2: return []
        if not is_prime(a) or not is_prime(b): return []
        c=b+2
        xm1=a*b*c-1
        am1=a-1
        bm1=b-1
        inc=2*a*b
        solutions=[]
        while c<limit:
            if is_prime(c):
                if xm1%am1==0 and xm1%bm1==0 and xm1%(c-1)==0:
                    solutions.append(c)
            c+=2
            xm1+=inc
        return solutions

    #---------------------------------------------------------------------------

    #a=727
    #b=1453
    #limit=500000
    #trials=10

    #start=clock()
    #for _ in xrange(trials):
    #    result=naive(a,b,limit)
    #end=clock()
    #print "Naive in",end-start,"seconds"
    #print result

    #start=clock()
    #for _ in xrange(trials):
    #    result=carmichael1(a,b,limit)
    #end=clock()
    #print "Carmichael1 in",end-start,"seconds"
    #print result

    #start=clock()
    #for _ in xrange(trials):
    #    result=carmichael2(a,b,limit)
    #end=clock()
    #print "Carmichael2 in",end-start,"seconds"
    #print result

    #start=clock()
    #for _ in xrange(trials):
    #    result=carmichael3(a,b,limit)
    #end=clock()
    #print "Carmichael3 in",end-start,"seconds"
    #print result

    #---------------------------------------------------------------------------

    #899331780481 = 239 * 409 * 1021 * 9011

    #a=239
    #b=409
    #c=1021
    #limit=10000

    #start=clock()
    #for _ in xrange(trials):
    #    result=carmichael(a,b,c,limit)
    #end=clock()
    #print "Carmichael (redirection) in",end-start,"seconds"
    #print result

    #Naive in 2.19843932679 seconds
    #[2179, 3631, 10891, 70423, 352111]
    #Carmichael in 0.0035508004509 seconds
    #[mpz(2179), mpz(3631), mpz(10891), mpz(70423), mpz(352111)]
    #Carmichael2 in 0.00424956244439 seconds
    #[mpz(2179), mpz(3631), mpz(10891), mpz(70423), mpz(352111)]
    #Carmichael3 in 0.00353201314692 seconds
    #[mpz(2179), mpz(3631), mpz(10891), mpz(70423), mpz(352111)]
    #---------------------------------------------------------------------------
    #from carmichaels import cdic

    #k=cdic.keys()
    #k.sort()
    #testlist=[]
    #for c in k:
    #    if len(cdic[c])==3:
    #        testlist.append((cdic[c][0],cdic[c][1]))
    #start=clock()
    #limit=1000000
    #result=[]
    #for test in testlist:
    #    a=test[0]
    #    b=test[1]
    #    result.append((a,b,carmichael1(a,b,limit)))
    #end=clock()
    #print result
    #print "Carmichael1: All triples < 10^12 ( 1000 numbers ) in",end-start,"seconds"
    #result=[]
    #for test in testlist:
        #a=test[0]
        #b=test[1]
        #result.append((a,b,naive(a,b,limit)))
    #end=clock()
    #print result
    #print "Naive: All triples < 10^12 ( 1000 numbers ) in",end-start,"seconds"

    #Carmichael1: All triples < 10^12 in 0.764858592363 seconds
    #Naive: All triples < 10^12 in 373.157365461 seconds
    #---------------------------------------------------------------------------
    #Print maximum number of factors found in cdic
    #from carmichaels import cdic
    #print reduce(lambda a,b: max(a,b), (len(cdic[c]) for c in cdic))
