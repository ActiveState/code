# Public domain.
import numpy

def array_from_iter(it, typecode):
    try:
        ans = numpy.array([it.next()], typecode)
    except StopIteration:
        raise ValueError('iterator contains 0 items')
    shape0 = ans.shape[1:]
    for (i, x) in enumerate(it):
        ans.resize((i+2,)+shape0)
        ans[i+1] = x
    return ans

def f():
  yield [1,2,3]
  yield [4,5,6]

print array_from_iter(f(), 'b')  # Prints [[1,2,3],[4,5,6]]

# Alternatively, the same code above works with numarray and Numeric.
# Just replace 'numpy' with 'numarray' or 'Numeric'.
