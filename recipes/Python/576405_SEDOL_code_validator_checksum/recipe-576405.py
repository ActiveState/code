'''
Copied by author from: http://paddy3118.blogspot.com/2008/08/sedol.html
From: http://en.wikipedia.org/wiki/SEDOL
SEDOLs are seven characters in length, consisting of two parts:
  a six-place alphanumeric code and a trailing check digit. 
'''

import string

# constants
sedolchars = string.digits + string.ascii_uppercase
sedol2value = dict((ch, n) for n,ch in enumerate(sedolchars))
for ch in 'AEIOU':
    del sedol2value[ch]
sedolchars = sorted(sedol2value.keys())
sedolweight = [1,3,1,7,3,9,1]

def check(sedol):
    return len(sedol) == 7 and \
           all(ch in sedolchars for ch in sedol) and \
           sum(sedol2value[ch] * sedolweight[n]
               for n,ch in enumerate(sedol)
               ) % 10 == 0

def checksum(sedol):
    tmp = sum(sedol2value[ch] * sedolweight[n]
               for n,ch in enumerate(sedol[:6])
               )
    return sedolchars[ (10 - (tmp % 10)) % 10]

sedol = '0263494'
print sedol, check(sedol), checksum(sedol)

print

# From: http://www.rosettacode.org/wiki/SEDOL
for sedol in '''
    710889
    B0YBKJ
    406566
    B0YBLH
    228276
    B0YBKL
    557910
    B0YBKR
    585284
    B0YBKT
    '''.split():
    print sedol + checksum(sedol)
