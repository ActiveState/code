#$Id: $

from sets import Set
import re

""" 
From the SWI-Prolog manual:
dwim_match(+Atom1, +Atom2)

       Succeeds if Atom1 matches Atom2 in `Do What I Mean' sense. Both
       Atom1 and Atom2 may also be integers or floats. The two atoms
       match if:

        o They are identical
        o They differ by one character (spy == spu)
        o One character is inserted/deleted (debug == deug)

        o Two characters are transposed (trace == tarce)

        o `Sub-words' are glued differently (existsfile == existsFile
        == exists_file)

        o Two adjacent sub words are transposed (existsFile == fileExists)

Thanks for M.L. Hetland for writing a Levenshtein Distance function in Py.
Thanks to Bijan Parsia for pointing me to SWI-Prolog's DWIM algo.
"""

def dwim_match(s1, s2, degree=1): #passing a degree arg sounds nice, but is
                                  #probably dumb... the rest of the code will
                                  #break if degree != 1... needs to be reworked
    #the easy, obvious case
    if s1 == s2:
        return True

    #covers these cases:
    # - one character of diff
    # - one character inserted/deleted
    if ld(s1, s2) == degree:
        return True

    #transposition is trickier since it's ld == 2; so, maybe:
    if ld(s1, s2) == 2:
        if len(s1) == len(s2):
            return True #this fails on "pat" and "atp"

    #the two subword cases: diff gluings; transp'd adjacents
    w1 = split_words(s1)
    w2 = split_words(s2)

    if w1 and w2: #diff gluings
        if len(w1) == len(w2):
            if Set(map(lambda s: s.lower(), w1)) == Set(map(lambda s: s.lower(), w2)):
                return True #this may cover both subword cases!?
                            #for now, let's say it does....
    #give up
    return False

def split_words(s, other=False):
    # we consider 4 word separator cases:
    #  "_", "-", "+", camelCase; short of running through a dictionary, I don't
    #  know how to do the no separator case: foobar...
    if "_" in s: sep = "_"
    if "-" in s: sep = "-"
    if "+" in s: sep = "+"
    if other and other in s:
        sep = other
    try:
        if sep:
            return s.split(sep)
    except UnboundLocalError:
        return case_splitter(s)

def case_splitter(s):
    pattern = re.compile(r"""([A-Z][a-z]*)""")
    def nullp(str):
        if str != "": return True
        else: return False
    return filter(nullp, pattern.split(s))

def ld(a, b): #stolen from m.l. hetland
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
    current = xrange(n+1)
    for i in xrange(1,m+1):
        previous, current = current, [i]+[0] * m
        for j in xrange(1, n+1):
            add, delete = previous[j] + 1, current[j-1] + 1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change +=1
            current[j] = min(add, delete, change)
    return current[n]

if __name__ == "__main__":


    s1 = s2 = "foobar"

    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)

    s1 = "spy"; s2 = "spu"
    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "debug"; s2 = "deug"
    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "file_exists"; s2 = "file-exists"

    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "file+exists"; s2 = "file-exists"

    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "Bartles"; s2 = "bartles"
    
    print "Testing: %s,  %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "fileExists"; s2 = "existsFile"

    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
    
    s1 = "bartles"; s2 = "james"

    print "Testing: %s, %s" % (s1, s2)
    print dwim_match(s1, s2)
