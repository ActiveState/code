def partition(it):
    for i in range(len(it)):
        if i == len(it) - 1:
            yield [it[0:i+1]]
        else:                     
            for p in partition(it[i+1:]):
                yield [it[0:i+1]] + p


print list(partition(range(4)))

[[0], [1], [2], [3]]
[[0], [1], [2, 3]]
[[0], [1, 2], [3]]
[[0], [1, 2, 3]]
[[0, 1], [2], [3]]
[[0, 1], [2, 3]]
[[0, 1, 2], [3]]
[[0, 1, 2, 3]]
