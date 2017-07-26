import operator
import types
import copy

class NoModifyError(RuntimeError): pass

class Constant:
  # Standard Functions
  def __init__(self, obj):
    if type(obj) is types.InstanceType and        issubclass(obj.__class__, Constant):
      raise TypeError, "Cannot wrap constant in constant"
    else:
      self.__dict__["_value"] = obj
  def __repr__(self):
    return repr(self._value)
  def __str__(self):
    return str(self._value)
  def __cmp__(self, x):
    return cmp(self._value, x)
  def __hash__(self):
    return hash(self._value)
  def __call__(self, *args):
    return apply(self._value, args)
  def __getattr__(self, x):
    print repr(x)
    print self.__dict__, self.__dict__.keys()
    if self.__dict__.has_key(x):
      return self.__dict__[x]
    elif Constant.__dict__.has_key(x):
      return Constant.__dict__[x]
    else:
      raise RuntimeError
      return getattr(self._value, x)
  def __setattr__(self, x, y):
    raise NoModifyError, "Cannot set attribute on constant object."
  def __delattr__(self, x):
    raise NoModifyError, "Cannot delete attribute of constant object."
  
  # List Functions
  def __len__(self):
    return len(self._value)
  def __getitem__(self, x):
    return self._value[x]
  def __setitem__(self, x, y):
    raise NoModifyError, "Cannot modify constant."
  def __delitem__(self, x):
    raise NoModifyError, "Cannot modify constant."
  def __getslice__(self, x, y):
    return self._value[x:y]
  def __setslice__(self, x, y, z):
    raise NoModifyError, "Cannot modify constant."
  def __delslice__(self, x, y):
    raise NoModifyError, "Cannot modify constant."
  def __contains__(self, x):
    return x in self._value
  def __nonzero__(self):
    if self._value: return 1
    else: return 0
        
  # Type Conversions
  def __coerce__(self, other):
    c = coerce(self._value, other)
    return (copy.deepcopy(c[0]), c[1])
  def __int__(self):
    return int(self._value)
  def __long__(self):
    return long(self._value)
  def __float__(self):
    return float(self._value)
  def __oct__(self):
    return oct(self._value)
  def __hex__(self):
    return hex(self._value)
  
class DeepConstant(Constant):
  def __getattr__(self, x):
    return Constant(getattr(self._value))
  def __getitem__(self, x):
    return Constant(self._value[x])
  def __getslice__(self, x, y):
    return Constant(self._value[x:y])
