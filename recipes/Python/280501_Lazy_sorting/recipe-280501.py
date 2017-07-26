import heapq

def isorted(iterable):
    lst = list(iterable)
    heapq.heapify(lst)
    pop = heapq.heappop
    while lst:
        yield pop(lst)
