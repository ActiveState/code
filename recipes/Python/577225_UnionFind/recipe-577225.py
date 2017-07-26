"""
MakeSet(x) initializes disjoint set for object x
Find(x) returns representative object of the set containing x
Union(x,y) makes two sets containing x and y respectively into one set

Some Applications:
- Kruskal's algorithm for finding minimal spanning trees
- Finding connected components in graphs
- Finding connected components in images (binary)
"""

def MakeSet(x):
     x.parent = x
     x.rank   = 0

def Union(x, y):
     xRoot = Find(x)
     yRoot = Find(y)
     if xRoot.rank > yRoot.rank:
         yRoot.parent = xRoot
     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot
     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot
         xRoot.rank = xRoot.rank + 1

def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent

""""""""""""""""""""""""""""""""""""""""""
# sample code using Union-Find (not needed)

import itertools

class Node:
    def __init__ (self, label):
        self.label = label
    def __str__(self):
        return self.label
    
l = [Node(ch) for ch in "abcdefg"]      #list of seven objects with distinct labels
print ""
print "objects labels:\t\t\t", [str(i) for i in l]

[MakeSet(node) for node in l]       #starting with every object in its own set

sets =  [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

assert( Find(l[0]) != Find(l[2]) )
Union(l[0],l[2])        #joining first and third
assert( Find(l[0]) == Find(l[2]) )

assert( Find(l[0]) != Find(l[1]) )
assert( Find(l[2]) != Find(l[1]) )
Union(l[0],l[1])        #joining first and second
assert( Find(l[0]) == Find(l[1]) )
assert( Find(l[2]) == Find(l[1]) )

Union(l[-2],l[-1])        #joining last two sets
Union(l[-3],l[-1])        #joining last two sets

sets = [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

for o in l:
    del o.parent
