import listmixin     # Uses recipe 440656
import array

# Public domain
class BitList(listmixin.ListMixin):
  """
  List of bits.

  The constructor takes a list or string containing zeros and ones,
  and creates an object that acts like list().

  This class is memory compact (uses 1 byte per every 8 elements).
  """
  def __init__(self, other=()):
    self.data = array.array('B')
    self.length = len(other)
    if hasattr(other, 'capitalize'):
      # Initialize from string.
      for i in xrange((len(other) + 7) // 8):
        c = other[i*8:(i+1)*8]
        byte = 0
        for j in xrange(len(c)):
          if c[j] != '0':
            byte |= 1<<j
        self.data.append(byte)
    else:
      # Initialize from sequence.
      for i in xrange((len(other) + 7) // 8):
        c = other[i*8:(i+1)*8]
        byte = 0
        for j in xrange(len(c)):
          if c[j]:
            byte |= 1<<j
        self.data.append(byte)

  def _constructor(self, iterable):
    return BitList(iterable)

  def __len__(self):
    return self.length

  def _get_element(self, i):
    return (self.data[i>>3]>>(i&7))&1

  def _set_element(self, i, x):
    index = i>>3
    mask  = (1<<(i&7))
    if x and x != '0':
      if not self.data[index] & mask:
        self.data[index] |= mask
    else:
      if self.data[index] & mask:
        self.data[index] ^= mask

  def _resize_region(self, start, end, new_size):
    """
    Resize slice self[start:end] so that it has size new_size.
    """
    old_size = end - start
    if new_size == old_size:
      return
    elif new_size > old_size:
      delta = new_size - old_size
      self.length += delta
      add_bytes = (self.length + 7) // 8 - len(self.data)
      self.data.extend(array.array('B', [0] * add_bytes))
      for i in xrange(self.length-1, start+new_size-1, -1):
        self._set_element(i, self._get_element(i - delta))
    elif new_size < old_size:
      delta = old_size - new_size
      for i in xrange(start+new_size, self.length-delta):
        self._set_element(i, self._get_element(i + delta))
      self.length -= delta
      del_bytes = len(self.data) - (self.length + 7) // 8
      assert del_bytes <= len(self.data)
      del self.data[len(self.data)-del_bytes:]

  def __getstate__(self):
    return (self.to_binary(), len(self))

  def __setstate__(self, (data, length)):
    self.__init__()
    self[:] = BitList.from_binary(data, length)

  def to_binary(self):
    """
    Return base256_binary_str.
    """
    return self.data.tostring()

  def from_binary(base256_binary_str, num_bits):
    """
    Return new BitList from base256_binary_str and number of bits.
    """
    ans = BitList()
    if len(base256_binary_str) != (num_bits+7)//8:
      raise ValueError('invalid length')
    ans.length = int(num_bits)
    ans.data = array.array('B')
    ans.data.fromstring(base256_binary_str)
    return ans

  from_binary = staticmethod(from_binary)

  def set_bit(self, i, x):
    """
    Set bit i to x (extending to the right with zeros if needed).
    """
    i = int(i)
    if i >= len(self):
      self.extend([0] * (i + 1 - len(self)))
    self[i] = x

  def get_bit(self, i):
    """
    Get bit i (or zero if i >= len(self)).
    """
    i = int(i)
    if i >= len(self):
      return 0
    return self[i]
