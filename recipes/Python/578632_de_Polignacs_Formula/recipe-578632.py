# Author: Samuel J Erickson
# Date: 8/9/2013
# Description: de Polignac's formula gives all factors of p in n! for any prime
# p.


def polignac(num,p):
    """
    input: num can be any positive integer and p and prime number.

    output: Gives the total number of factors of p in num! (num factorial).
    Stated another way, this function returns the total number of factors
    of p of all numbers between 1 and num; de Polignac's formula is pretty 
    nifty if you are into working with prime numbers.
    """
    factorsDict={}
    if num>1 and p==1:
        print("Invalid entry since 1 is the identity.")
    else:
        while num>1:
            factorsDict[num//p]=num//p
            num=num//p
        return sum(factorsDict)
