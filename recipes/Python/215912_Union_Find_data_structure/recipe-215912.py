'''
unionfind.py

A class that implements the Union Find data structure and algorithm.  This
data structure allows one to find out which set an object belongs to, as well
as join two sets.

The algorithm's performance, given m union/find operations of any ordering, on
n elements has been shown to take log* time per operation, where log* is
pronounced log-star, and is the INVERSE of what is known as the Ackerman
function, which is given below:
A(0) = 1
A(n) = 2**A(n-1)

I include the functions to be complete.  Note that we can be 'inefficient'
when performing the inverse ackerman function, as it will only take a maximum
of 6 iterations to perform; A(5) is 65536 binary digits long (a 1 with 65535
zeroes following).  A(6) is 2**65536 binary digits long, and cannot be
represented by the memory of the entire universe.


The Union Find data structure is not a universal set implementation, but can
tell you if two objects are in the same set, in different sets, or you can
combine two sets.
ufset.find(obja) == ufset.find(objb)
ufset.find(obja) != ufset.find(objb)
ufset.union(obja, objb)


This algorithm and data structure are primarily used for Kruskal's Minimum
Spanning Tree algorithm for graphs, but other uses have been found.

August 12, 2003 Josiah Carlson
'''

def Ackerman(inp, memo={0:1}):
	inp = max(int(inp), 0)
	if inp in memo:
		return memo[inp]
	elif inp <= 5:
		memo[inp] = 2**ackerman(inp-1)
		return memo[inp]
	else:
		print "Such a number is not representable by all the subatomic\nparticles in the universe."
		ackerman(4);
		out = (inp-4)*"2**" + str(memo[4])
		print out
		raise Exception, "NumberCannotBeRepresentedByAllSubatomicParticlesInUniverse"

def inverseAckerman(inp):
    t = 0
    while Ackerman(t) < inp:
        t += 1
    return t


class UnionFind:
    def __init__(self):
        '''\
Create an empty union find data structure.'''
        self.num_weights = {}
        self.parent_pointers = {}
        self.num_to_objects = {}
        self.objects_to_num = {}
        self.__repr__ = self.__str__
    def insert_objects(self, objects):
        '''\
Insert a sequence of objects into the structure.  All must be Python hashable.'''
        for object in objects:
            self.find(object);
    def find(self, object):
        '''\
Find the root of the set that an object is in.
If the object was not known, will make it known, and it becomes its own set.
Object must be Python hashable.'''
        if not object in self.objects_to_num:
            obj_num = len(self.objects_to_num)
            self.num_weights[obj_num] = 1
            self.objects_to_num[object] = obj_num
            self.num_to_objects[obj_num] = object
            self.parent_pointers[obj_num] = obj_num
            return object
        stk = [self.objects_to_num[object]]
        par = self.parent_pointers[stk[-1]]
        while par != stk[-1]:
            stk.append(par)
            par = self.parent_pointers[par]
        for i in stk:
            self.parent_pointers[i] = par
        return self.num_to_objects[par]
    def union(self, object1, object2):
        '''\
Combine the sets that contain the two objects given.
Both objects must be Python hashable.
If either or both objects are unknown, will make them known, and combine them.'''
        o1p = self.find(object1)
        o2p = self.find(object2)
        if o1p != o2p:
            on1 = self.objects_to_num[o1p]
            on2 = self.objects_to_num[o2p]
            w1 = self.num_weights[on1]
            w2 = self.num_weights[on2]
            if w1 < w2:
                o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1
            self.num_weights[on1] = w1+w2
            del self.num_weights[on2]
            self.parent_pointers[on2] = on1
    def __str__(self):
        '''\
Included for testing purposes only.
All information needed from the union find data structure can be attained
using find.'''
        sets = {}
        for i in xrange(len(self.objects_to_num)):
            sets[i] = []
        for i in self.objects_to_num:
            sets[self.objects_to_num[self.find(i)]].append(i)
        out = []
        for i in sets.itervalues():
            if i:
                out.append(repr(i))
        return ', '.join(out)

if __name__ == '__main__':
    print "Testing..."
    uf = UnionFind()
    az = "abcdefghijklmnopqrstuvwxyz"
    az += az.upper()
    uf.insert_objects(az)
    import random
    cnt = 0
    while len(uf.num_weights) > 20:
        cnt += 1
        uf.union(random.choice(az), random.choice(az))
    print uf, cnt
    print "Testing complete."
