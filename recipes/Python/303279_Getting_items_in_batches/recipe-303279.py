from itertools import islice, chain

def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)


seq = xrange(19)
for batchiter in batch(seq, 3):
    print "Batch: ",
    for item in batchiter:
        print item,
    print

Batch:  0 1 2
Batch:  3 4 5
Batch:  6 7 8
Batch:  9 10 11
Batch:  12 13 14
Batch:  15 16 17
Batch:  18
