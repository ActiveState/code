import math

def sum_with_partials(arr):
  size = len(arr)
  iters = math.ceil(math.log(size)/math.log(2))
  for itr in range(int(iters)):
    step = 2**itr
    for i in xrange(0, size, 2**(itr+1)):
      next_i = i+step
      if next_i<size:
        arr[i]+=arr[next_i]
  return arr[0]
