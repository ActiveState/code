from random import *
from heapq import *

cmps = 0

class Int(int):
    def __lt__(self, other):
        global cmps
        cmps += 1
        return int.__lt__(self, other)
    def __le__(self, other):
        global cmps
        cmps += 1
        return int.__le__(self, other)

def count_cmps(f, data, k):
    'Count comparisons in a call to f(k, data)'
    global cmps
    data = data[:]
    shuffle(data)
    cmps = 0
    result = f(k, data)
    assert result[:10] == list(range(10))
    return cmps

# -------- variants of nsmallest -------

def heapifying_smallest(k, data):
    heapify(data)
    result = [heappop(data) for j in range(k)]
    data.extend(result)
    return result

def select_nth(data, n):
    if len(data) == 1:
        return data[0]
    pivot = choice(data)
    lhs, rhs = [], []
    for elem in data:
        (lhs if elem < pivot else rhs).append(elem)
    if len(lhs) >= n+1:
        return select_nth(lhs, n)
    else:
        return select_nth(rhs, n - len(lhs))

def selecting_smallest(k, data):
    pivot = select_nth(data, k)
    return sorted(elem for elem in data if elem <= pivot)[:k]

def partitioning_smallest(n, data):
    if len(data) <= 1:
        return data
    pivot = choice(data)
    lhs, rhs = [], []
    for elem in data:
        (lhs if elem <= pivot else rhs).append(elem)
    if n < len(lhs):
        return partitioning_smallest(n, lhs)
    else:
        return sorted(lhs) + partitioning_smallest(n - len(lhs), rhs)


if __name__ == '__main__':
    # compare nsmallest implementations
    n, k = 100000, 100
    print('n: %d\tk: %d' % (n, k))
    data = list(map(Int, range(n)))
    for f in [nsmallest, heapifying_smallest,
             selecting_smallest, partitioning_smallest]:
        counts = sorted(count_cmps(f, data, k) for i in range(5))
        print(counts, f.__name__)
