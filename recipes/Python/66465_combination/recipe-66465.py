#!/usr/bin/env python
__version__ = "1.1"
"""combination.py-- Efficient recursive functions for printing the
combination of the selected number of characters from the specified string.
Can generate unique or all possible combinations.

"""
import sys

def printList(alist):
    print ''.join(alist)

def printUniqueCombinations(alist, numb, blist=[]):
    if not numb: return printList(blist)
    for i in range(len(alist)):
        blist.append(alist[i])
        printUniqueCombinations(alist[i+1:], numb-1, blist)
        blist.pop()

def printCombinations(alist, numb, blist=[]):
    if not numb: return printList(blist)
    for i in range(len(alist)):
        blist.append(alist.pop(i))
        printCombinations(alist, numb-1, blist)
        alist.insert(i, blist.pop())

if __name__ == '__main__':
    k='love'
    n=2
    if len(sys.argv)>=2: k = sys.argv[1]
    if len(sys.argv)>=3: n = int(sys.argv[2])
    print 'combinations of %d letters in "%s" ' % (n, k)
    printCombinations(list(k), n)
    print 'unique combinations of %d letters in "%s" ' % (n, k)
    printUniqueCombinations(list(k), n)
