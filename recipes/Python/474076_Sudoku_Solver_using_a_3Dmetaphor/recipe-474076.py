"""
This code is placed in the public domain. The author 
can be reached at anton.vredegoor@gmail.com

Last edit: Anton Vredegoor, 22-02-2006

A sudoku problem is represented by a binary cube, 
the x and y coordinates are the rows and columns of
the original sudoku, the z-coordinate is the value
(the "height") of a point in the sudoku grid.

We wipe away points until there are n**4  (81 if we
start with parameter n=3) binary points left in the cube,
which do not share points in the same x,y,or z 
"sight line" or nxn,z block.

The sudoku17 file that is read from is a list of sudoku
problems with 17 givens and can be found at:

http://www.csse.uwa.edu.au/~gordon/sudokumin.php

Thanks Gordon, for making this list available.

In each line there are 81 digits in range(10) and a 
linefeed. Here is the first line (0 means "unknown"):

000000010400000000020000000\
000050407008000300001090000\
300400200050100000000806000

I used vpython while developing the code in order to
visualize what was going on in the cube (some simple
differently colored spheres in 3d space helped a lot), 
but the final script doesn't need it. Still, I am awed by 
vpythons 3D stereo mode which the "crosseyed"
visualization trick. Keep up the good work.

Uncomment this line in function "test" to see
the sudoku grid output: 

for sol in sols: print sol
"""

n = 3
n2 = n*n
n4 = n2*n2
B = range(n)
R = range(n2)

class Node:
    
    def __init__(self,possibles): 
        S = self.possibles = possibles #set of possible points (3-tuples)
        all = self.all = self.clean() #list of all *lists* of points
        valid = self.isvalid = len(S)>=n4 and len(all)==n4*4
        self.issolved = valid and len(S)==n4 and max(map(len,all))==1
    
    def clean(self):
        #eliminate points until stable
        S = self.possibles
        while True:
            L = {},{},{},{}
            for x,y,z in S:
                r,c = x//n,y//n
                for Q,T in zip(L,((x,y),(x,z),(y,z),(r,c,z))):
                    Q[T] = Q.get(T,[]) +[(x,y,z)]
            all = []
            for Q in L:
                all.extend(Q.values())
            ns = len(S)
            for x in all:
                if len(x) == 1:                    
                    S -= friends(x[0])
            if ns == len(S):
                break
        return all
        
    def children(self):
        if self.isvalid and not self.issolved:
            #heuristic: choose shortest list of points
            pts = min((len(x),x) for x in self.all if len(x)>1)[1]
            for p in pts:
                yield Node(self.possibles-friends(p))

    def __repr__(self):
        S = self.possibles
        M = [['_' for i in R] for j in R]
        for i,j,k in S:
            if not S&friends((i,j,k)):
                M[i][j] = str(k+1)
        return '\n'+'\n'.join(map(''.join,M))

def friends(point, memo = {}):
    #points in the same sight line or nxnxz block
    try:
        return memo[point]
    except KeyError:        
        x,y,z = point
        res = set()
        for i in R:
            res.update([(i,y,z),(x,i,z),(x,y,i)])
        a,b = x//n*n,y//n*n
        res |= set((a+i,b+j,z) for i in B for j in B)
        res.discard((x,y,z))
        memo[point] = res
    return res

def solutions(N):
    #depth first search
    if N.issolved:
        yield N
    else:
        for child in N.children():
            for g in solutions(child):
                yield g

def readstring(s):
    Z = zip([(i,j) for i in R for j in R],map(int,s))
    givens = set((i,j,k-1) for (i,j),k in Z if k)
    possibles = set((i,j,k) for i in R for j in R for k in R)
    for p in givens:
        possibles -= friends(p)
    return possibles
        
def test():
    for i,line in enumerate(file('sudoku17')):
        N = Node(readstring(line.strip()))
        sols = list(solutions(N))
        if  i%10==0: print
        print i,
        #for sol in sols: print sol
        if len(sols) > 1:
            print 'more than one solution'
            break
        
if __name__=='__main__':
    test()
