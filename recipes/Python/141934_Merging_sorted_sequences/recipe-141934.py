def xmerge(*ln):
     """ Iterator version of merge.
 
     Assuming l1, l2, l3...ln sorted sequences, return an iterator that
     yield all the items of l1, l2, l3...ln in ascending order.
     Input values doesn't need to be lists: any iterable sequence can be used.
     """
     pqueue = []
     for i in map(iter, ln):
         try:
             pqueue.append((i.next(), i.next))
         except StopIteration:
             pass
     pqueue.sort()
     pqueue.reverse()
     X = max(0, len(pqueue) - 1)
     while X:
         d,f = pqueue.pop()
         yield d
         try:
             # Insort in reverse order to avoid pop(0)
             lo, hi, d = 0, X, f()
             while lo < hi:
                 mid = (lo+hi)//2
                 if d > pqueue[mid][0]: hi = mid
                 else: lo = mid+1
             pqueue.insert(lo, (d,f))
         except StopIteration:
             X-=1
     if pqueue:
         d,f = pqueue[0]
         yield d
         try:
             while 1: yield f()
         except StopIteration:pass
 
 
def merge(*ln):
     """ Merge several sorted sequences into a sorted list.
     
     Assuming l1, l2, l3...ln sorted sequences, return a list that contain
     all the items of l1, l2, l3...ln in ascending order.
     Input values doesn't need to be lists: any iterable sequence can be used.
     """
     return list(xmerge(*ln))
