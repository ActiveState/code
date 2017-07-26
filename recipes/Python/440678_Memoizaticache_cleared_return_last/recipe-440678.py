import cPickle

# Public domain.
def memoize(f):
  """
  Memoize function, clear cache on last return.
  """
  count = [0]
  cache = {}
  def g(*args, **kwargs):
    count[0] += 1
    try:
      try:
        if len(kwargs) != 0: raise ValueError
        hash(args)
        key = (args,)
      except:
        key = cPickle.dumps((args, kwargs))
      if key not in cache:
        cache[key] = f(*args, **kwargs)
      return cache[key]
    finally:
      count[0] -= 1
      if count[0] == 0:
        cache.clear()
  return g


# Example usage

def fib(n):
  if n in [0, 1]: return n
  return fib(n-1)+fib(n-2)

fib = memoize(fib)

print fib(300)
