#!usr/bin/python
#FileName: sieve_once_again.py
#Python Version: 2.6.2
#Author: Rahul Raj
#Sat May 15 11:41:21 2010 IST


fi=0 #flag index for scaling with big numbers..
n=input('Prime Number(>2) Upto:')
s=range(3,n,2)

def next_non_zero():
    "To find the first non zero element of the list s"
    global fi,s
    while True:
        if s[fi]:return s[fi]
        fi+=1

def sieve():
    primelist=[2]
    limit=(s[-1]-3)/2
    largest=s[-1]

    while True:
        m=next_non_zero()
        fi=s.index(m)
        if m**2>largest:
            primelist+=[prime for prime in s if prime] #appending rest of the non zero numbers
            break
        ind=(m*(m-1)/2)+s.index(m)
        primelist.append(m)
        while ind<=limit:
            s[ind]=0
            ind+=m
        s[s.index(m)]=0

    #print primelist
    print 'Number of Primes upto %d: %d'%(n,len(primelist))
    
if __name__=='__main__':
    sieve()
    
