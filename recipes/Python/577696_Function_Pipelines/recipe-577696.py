class Pipeline(object):
  def __init__(self, _func_list=None):
    if _func_list is None:
      _func_list = []
    self._func_list = _func_list

  def __call__(self, *args, **kwargs):
    f = None
    while f == None:
      try:
        f = self.pop(0)
      except IndexError:
        raise StopIteration()

      if callable(f):
        return f(self, *args, **kwargs)
      else:
        f = None

  def __iter__(self):
    for f in self._func_list:
      yield f

  def __eq__(self, other):
    return self._func_list == other._func_list

  def __add__(self, other):
    return Pipeline(self._func_list + list(other))

  def push(self, f):
    return self._func_list.insert(0, f)

  def pop(self, *args, **kwargs):
    return self._func_list.pop(*args, **kwargs)

  def append(self, *args, **kwargs):
    return self._func_list.append(*args, **kwargs)


if __name__ == '__main__':
  def add_1(pipeline, x):
    return pipeline(x + 1)

  def mul_2(pipeline, x):
    return pipeline(x * 2)

  def identity(pipeline, x):
    return x

  p = Pipeline([add_1, mul_2, add_1, mul_2, identity])
  print p(1)
  # 10
