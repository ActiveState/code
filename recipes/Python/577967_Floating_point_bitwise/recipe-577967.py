"""This module defines bitwise operations on floating point numbers by pretending that they consist of an infinite sting of bits extending to the left as well as to the right.
More precisely the infinite string of bits b = [...,b[-2],b[-1],b[0],b[1],b[2],...] represents the number x = sum( b[i]*2**i for i in range(-inf,inf) ). Negative numbers are represented in one's complement. The identity 0.111... == 1.0 creates an ambiquity in the representation. To avoid it positive numbers are defined to be padded with zeros in both directions while negative numbers are padded with ones in both directions. This choice leads to the useful identity ~a == -a and allows +0 == ...000.000... to be the |-identity and -0 == ...111.111... to be the &-identity. Unfortunately the choice breaks compatibility with integer bitwise operations involving negative numbers."""

from math import frexp, copysign
from sys import float_info

__author__ = "Pyry Pakkanen"
__copyright__ = "Copyright 2011"
__credits__ = ["Pyry Pakkanen"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Pyry Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "initial release"

fmax, max_exp, max_10_exp, fmin, min_exp, min_10_exp, dig, mant_dig, epsilon, radix, rounds = float_info

def ifrexp(x):
    """Get the mantissa and exponent of a floating point number as integers."""
    m,e = frexp(x)
    return int(m*2**mant_dig),e

def float_not(a):
    """~a"""
    return -a

def float_and(a,b):
    """a & b"""
    if a==0.0:
        if copysign(1.0,a)==1.0:
            return 0.0
        else:
            return b
    if b==0.0:
        return float_and(b,a)

    if a<0 and b<0:
        return -float_or(-a,-b)

    if abs(a)>=abs(b):
        return float_and_(a,b)
    else:
        return float_and_(b,a)    

def float_or(a,b):
    """a | b"""
    if a==0.0:
        if copysign(1.0,a)==1.0:
            return b
        else:
            return -0.0
    if b==0.0:
        return float_or(b,a)

    if a<0 and b<0:
        return -float_and(-a,-b)
        
    if abs(a)>=abs(b):
        return float_or_(a,b)
    else:
        return float_or_(b,a)


def float_xor(a,b):
    """a ^ b"""
    if a==0.0:
        if copysign(1.0,a)==1.0:
            return b
        else:
            return -b
    if b==0.0:
        return float_xor(b,a)

    if a<0:
        if b<0:
            return float_xor(-a,-b)
        else:
            return -float_xor(-a,b)
    if b<0:
        return -float_xor(a,-b)
            
    if abs(a)>=abs(b):
        return float_xor_(a,b)
    else:
        return float_xor_(b,a)

#The helper functions assume that exponent(a) >= exponent(b).
#The operation lambda x: ~(-x) converts between two's complement and one's complement representation of a negative number. One's complement is more natural for floating point numbers because the zero is signed.

def float_and_(a,b):
    ma,ea = ifrexp(a)
    mb,eb = ifrexp(b)

    mb = mb>>(ea-eb)

    if ma<0:
        return ( mb&~(-ma) )*2**(ea-mant_dig)
    if mb<0:
        return ( ~(-mb)&ma )*2**(ea-mant_dig)
    return ( mb&ma )*2**(ea-mant_dig)

def float_or_(a,b):
    ma,ea = ifrexp(a)
    mb,eb = ifrexp(b)

    mb = mb>>(ea-eb)

    if ma<0:
        return ( -(~( mb|~(-ma) )) )*2**(ea-mant_dig)
    if mb<0:
        return ( -(~( ~(-mb)|ma )) )*2**(ea-mant_dig)
    return ( mb|ma )*2**(ea-mant_dig)

def float_xor_(a,b):
    ma,ea = ifrexp(a)
    mb,eb = ifrexp(b)

    mb = mb>>(ea-eb)

    return ( mb^ma )*2**(ea-mant_dig)
