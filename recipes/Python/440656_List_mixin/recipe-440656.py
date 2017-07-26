import copy
import sys

# Public domain
class ListMixin(object):
  """
  Defines all list operations from a small subset of methods.

  Subclasses should define _get_element(i), _set_element(i, value),
  __len__(), _resize_region(start, end, new_size) and
  _constructor(iterable).  Define __iter__() for extra speed.

  The _get_element() and _set_element() methods are given indices with
  0 <= i < len(self).

  The _resize_region() method should resize the slice self[start:end]
  so that it has size new_size.  It is given indices such that
  start <= end, 0 <= start <= len(self) and 0 <= end <= len(self).
  The resulting elements in self[start:start+new_size] can be set to
  None or arbitrary Python values.

  The _constructor() method accepts an iterable and should return a
  new instance of the same class as self, populated with the elements
  of the given iterable.
  """
  def __cmp__(self, other):
    return cmp(list(self), list(other))

  def __hash__(self):
    raise TypeError('list objects are unhashable')

  def __iter__(self):
    for i in xrange(len(self)):
      yield self._get_element(i)

  def _tuple_from_slice(self, i):
    """
    Get (start, end, step) tuple from slice object.
    """
    (start, end, step) = i.indices(len(self))
    # Replace (0, -1, 1) with (0, 0, 1) (misfeature in .indices()).
    if step == 1:
      if end < start:
        end = start
      step = None
    if i.step == None:
      step = None
    return (start, end, step)

  def _fix_index(self, i):
    if i < 0:
      i += len(self)
    if i < 0 or i >= len(self):
      raise IndexError('list index out of range')
    return i

  def __getitem__(self, i):
    if isinstance(i, slice):
      (start, end, step) = self._tuple_from_slice(i)
      if step == None:
        indices = xrange(start, end)
      else:
        indices = xrange(start, end, step)
      return self._constructor([self._get_element(i) for i in indices])
    else:
      return self._get_element(self._fix_index(i))

  def __setitem__(self, i, value):
    if isinstance(i, slice):
      (start, end, step) = self._tuple_from_slice(i)
      if step != None:
        # Extended slice
        indices = range(start, end, step)
        if len(value) != len(indices):
          raise ValueError(('attempt to assign sequence of size %d' +
                            ' to extended slice of size %d') %
                           (len(value), len(indices)))
        for (j, assign_val) in enumerate(value):
          self._set_element(indices[j], assign_val)
      else:
        # Normal slice
        if len(value) != (end - start):
          self._resize_region(start, end, len(value))
        for (j, assign_val) in enumerate(value):
          self._set_element(start + j, assign_val)
    else:
      # Single element
      self._set_element(self._fix_index(i), value)

  def __delitem__(self, i):
    if isinstance(i, slice):
      (start, end, step) = self._tuple_from_slice(i)
      if step != None:
        # Extended slice
        indices = range(start, end, step)
        # Sort indices descending
        if len(indices) > 0 and indices[0] < indices[-1]:
          indices.reverse()
        for j in indices:
          del self[j]
      else:
        # Normal slice
        self._resize_region(start, end, 0)
    else:
      # Single element
      i = self._fix_index(i)
      self._resize_region(i, i + 1, 0)

  def __add__(self, other):
    if isinstance(other, self.__class__):
      ans = self._constructor(self)
      ans += other
      return ans
    return list(self) + other

  def __mul__(self, other):
    ans = self._constructor(self)
    ans *= other
    return ans

  def __radd__(self, other):
    if isinstance(other, self.__class__):
      ans = other._constructor(self)
      ans += self
      return ans
    return other + list(self)

  def __rmul__(self, other):
    return self * other

  def __iadd__(self, other):
    self[len(self):len(self)] = other
    return self

  def __imul__(self, other):
    if other <= 0:
      self[:] = []
    elif other > 1:
      aux = list(self)
      for i in xrange(other-1):
        self.extend(aux)
    return self

  def append(self, other):
    self[len(self):len(self)] = [other]

  def extend(self, other):
    self[len(self):len(self)] = other

  def count(self, other):
    ans = 0
    for item in self:
      if item == other:
        ans += 1
    return ans

  def reverse(self):
    for i in xrange(len(self)//2):
      j = len(self) - 1 - i
      (self[i], self[j]) = (self[j], self[i])

  def index(self, x, i=0, j=None):
    if i != 0 or j is not None:
      (i, j, ignore) = self._tuple_from_slice(slice(i, j))
    if j is None:
      j = len(self)
    for k in xrange(i, j):
      if self._get_element(k) == x:
        return k
    raise ValueError('index(x): x not in list')

  def insert(self, i, x):
    self[i:i] = [x]

  def pop(self, i=None):
    if i == None:
      i = len(self)-1
    ans = self[i]
    del self[i]
    return ans

  def remove(self, x):
    for i in xrange(len(self)):
      if self._get_element(i) == x:
        del self[i]
        return
    raise ValueError('remove(x): x not in list')

  # Define sort() as appropriate for the Python version.
  if sys.version_info[:3] < (2, 4, 0):
    def sort(self, cmpfunc=None):
      ans = list(self)
      ans.sort(cmpfunc)
      self[:] = ans
  else:
    def sort(self, cmpfunc=None, key=None, reverse=False):
      ans = list(self)
      if reverse == True:
        ans.sort(cmpfunc, key, reverse)
      elif key != None:
        ans.sort(cmpfunc, key)
      else:
        ans.sort(cmpfunc)
      self[:] = ans

  def __copy__(self):
    return self._constructor(self)

  def __deepcopy__(self, memo={}):
    ans = self._constructor([])
    memo[id(self)] = ans
    ans[:] = copy.deepcopy(tuple(self), memo)
    return ans

  # Tracking idea from R. Hettinger's deque class.  It's not
  # multithread safe, but does work with the builtin Python classes.
  def __str__(self, track=[]):
    if id(self) in track:
      return '...'
    track.append(id(self))
    ans = '%r' % (list(self),)
    track.remove(id(self))
    return ans

  def __repr__(self):
    return self.__class__.__name__ + '(' + str(self) + ')'


# Example usage:

class TestList(ListMixin):
  def __init__(self, L=[]):
    self.L = list(L)

  def _constructor(self, iterable):
    return TestList(iterable)

  def __len__(self):
    return len(self.L)

  def _get_element(self, i):
    assert 0 <= i < len(self)
    return self.L[i]

  def _set_element(self, i, x):
    assert 0 <= i < len(self)
    self.L[i] = x

  def _resize_region(self, start, end, new_size):
    assert 0 <= start <= len(self)
    assert 0 <= end   <= len(self)
    assert start <= end
    self.L[start:end] = [None] * new_size

# Now TestList() has behavior identical to that of list().
