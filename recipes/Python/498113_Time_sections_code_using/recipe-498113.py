# Public domain

from __future__ import with_statement
import contextlib, time

@contextlib.contextmanager
def accum_time(L):
  """
  Add time used inside a with block to the value of L[0].
  """
  start = time.clock()
  try:
    yield
  finally:
    end = time.clock()
    L[0] += end - start

# Example: measure time to execute code inside with blocks.
t = [0]
with accum_time(t):
  print sum(range(1000000))
with accum_time(t):
  print sum(range(2000000))
print 'Time:', t[0]
