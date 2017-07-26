rows, cols = 3, 100000

A = np.random.randn(rows, cols)
B = [list(n) for n in A]

start = time()
i = np.argsort(A[0])
for n in xrange(len(A)):
    A[n] = A[n][i]
print time() - start


start = time()
zipped = zip(*B)
zipped.sort()
B = zip(*zipped)
print time() - start
