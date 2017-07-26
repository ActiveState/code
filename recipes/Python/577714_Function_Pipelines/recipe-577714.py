class Pipeline(object):
  def __init__(self, *args):
    if args:
      self._func_list=args
    else:
      self._func_list=[]

  def __call__(self, *args, **kwargs):
    (fargs,fkwargs) = (args,kwargs)
    for f in self:
      results = f(*fargs, **fkwargs)
      if isinstance(results, tuple) and len(results) == 2 and \
              isinstance(results[0],list) and isinstance(results[1],dict):
        fargs,kwargs = results
      else:
        fargs = [results]
        fkwargs = {}
    return results

  def __iter__(self):
    for f in self._func_list:
      yield f
    raise StopIteration

  def __eq__(self, other):
    return self._func_list == other._func_list

  def __add__(self, other):
    funcs = other
    if callable(other):
       funcs = [other] 
    args = list(self._func_list) + list(funcs)
    return Pipeline(*args)

  def push(self, f):
    return self._func_list.insert(0, f)

  def pop(self, *args, **kwargs):
    return self._func_list.pop(*args, **kwargs)

  def append(self, *args, **kwargs):
    return self._func_list.append(*args, **kwargs)


if __name__ == '__main__':
  def add_1(x):
    return x+1

  def mul_2(x):
    return (x * 2)

  def identity(x):
    return x

  p = Pipeline(add_1, mul_2, add_1, mul_2, identity)
  assert(p(1) == 10)
  
  p = p + mul_2
  assert(p(1) == 20)

  q = Pipeline(p, add_1, add_1)
  assert(q(1) == 22)

  r = Pipeline(add_1)
  s = Pipeline(add_1)
  t = r + s

  assert(t(1) == 3)
