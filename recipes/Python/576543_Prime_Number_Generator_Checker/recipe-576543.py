#
# prime number generator
# This program gets two number as input
# and prints
#       Prime numbers in the range
#       Actual number of primes in the range
#   and Estimation based on formula
#                     n
#           pi(n)= -------
#                   log(n)
#           pi(n)=number of primes less than n
#

from math import *
def isPrime(n):
    if n%2==0 and n!=2:return False    #if number is EVEN AND it is NOT 2

    k = n**0.5 ;  m = ceil(k)          #if number is PERFECT SQUARE
    if k==m:return False
    
    for i in xrange(3,int(m),2):       #divisibility test ODDS ONLY
        if n%i==0:return False
        
    return True                        #otherwise it is PRIME

if __name__=='__main__':
    s = input('Enter Start: ')
    e = input('Enter End:   ')
    s|=1                               #if s%2==0:s+=1   # ODDS only
    list = [x for x in range(s,e,2) if isPrime(x)] 
    print list,'\n',len(list),'\n',int(ceil(e/log(e)-s/log(s)))
    #prints list of primes , length of list , estimate using the formula
    
