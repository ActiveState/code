from collections import defaultdict

class Partition:

    def __init__(self, S):
        self.data = list(S)
        self.m = len(S)
        self.table = self.rgf_table()

    def __getitem__(self, i):
        #generates set partitions by index
        if i > len(self) - 1:
             raise IndexError
        L =  self.unrank_rgf(i)
        result = self.as_set_partition(L)
        return result
    
    def __len__(self):
        return self.table[self.m,0]

    def as_set_partition(self, L):
        # Transform a restricted growth function into a partition
        n = max(L[1:]+[1])
        m = self.m
        data = self.data
        P = [[] for _ in range(n)]
        for i in range(m):
            P[L[i+1]-1].append(data[i])
        return P

    def rgf_table(self):
        # Compute the table values 
        m = self.m
        D = defaultdict(lambda:1)
        for i in range(1,m+1):
            for j in range(0,m-i+1):
                D[i,j] = j * D[i-1,j] + D[i-1,j+1]
        return D

    def unrank_rgf(self, r):
        # Unrank a restricted growth function
        m = self.m
        L = [1 for _ in range(m+1)]
        j = 1
        D = self.table
        for i in range(2,m+1):
            v = D[m-i,j]
            cr = j*v
            if cr <= r:
                L[i] = j + 1
                r -= cr
                j += 1
            else:
                L[i] = r / v + 1
                r  %= v
        return L

def test():
    S = set(range(4))
    P = Partition(S)
    print len(P)
    for x in P:
         print x

if __name__ == '__main__':
    test() 
