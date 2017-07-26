def heapify(array, start, end, cmp): # array is almost a heap (except the root)
    root = start
    while root * 2 + 1 < end:
        child = root * 2 + 1
        if child + 1 < end:
            v, k = cmp((array[root], root), (array[child], child), (array[child + 1], child + 1))
        else:
            v, k = cmp((array[root], root), (array[child], child))
        if not k == root:
            array[root], array[k] = array[k], array[root]
            root = k
        else:
            break

def build_heap_max(array):
    length = len(array)
    for i in xrange(length / 2, -1, -1):
        heapify(array, i, length, max)

def heap_sort(array):
    build_heap_max(array)
    size = len(array)
    while size > 0:
        array[0], array[size - 1] = array[size - 1], array[0]
        heapify(array, 0, size - 1, max)
        size -= 1
