# striplist.py

# Take a list of string objects and return the same list
# stripped of extra whitespace.

def striplist(l):
    return([x.strip() for x in l])

# This may look a bit more elegant, but it is significantly slower than
# striplist(). This may be dur to the fact that it's using the string.strip()
# method.

from string import strip
def inefficient(l):
    return(map(strip, l))
del strip
# Another version of inefficient() using builtin strip()
def inefficient_as_well(l):
    return(map(lambda x: x.strip(), l))

# This is only slightly slower than or comparable to striplist()
def comparable(l)
    for x in xrange(len(l)):
        l[x] = l[x].strip()
    return(l)

# This is also on the same order as both comparabale() & striplist()
def comparable_as_well(l)
    tmp = []
    for x in len(l):
        tmp.append(x.strip())
    return(tmp)

# An example of a class that would have the strip method.  It inherits
# everything from "list", and adds a method, .strip()
# This is slower than striplist()

class StrippableList(list):
    def __init__(self,l=[]):
        list.__init__(self,l)
    def strip(self,char=None):
        return(StrippableList([x.strip(char) for x in self]))
