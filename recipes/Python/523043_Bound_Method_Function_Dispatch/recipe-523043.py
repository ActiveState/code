class RPN_Evaluator(object):

  def __init__(self):
    self.stack = []

  def push(self, x):
    self.stack.append(x)

  def pop(self):
    return self.stack.pop() if self.stack else 0

  def result(self):
    return self.stack[:]

  operations = {}

  assign = lambda d, k: lambda f: d.setdefault(k, f)

  @assign(operations, '+')
  def plus(self, a, b):
    return a + b

  @assign(operations, '-')
  def minus(self, a, b):
    return a - b

  @assign(operations, '*')
  def mult(self, a, b):
    return a * b

  @assign(operations, '/')
  def div(self, a, b):
    return a / b

  def dispatch(self, k, *args, **kwds):
    try:
      method = self.operations[k].__get__(self, type(self))
    except KeyError:
      assert k in self.operations, "invalid operation: " + repr(k)
    return method(*args, **kwds)

  def eval(self, rpn):
    for x in str(rpn).split():
      try:
        value = int(x)
      except ValueError:
        b = self.pop()
        a = self.pop()
        value = self.dispatch(x, a, b)
      self.push(value)
    return self.result()

calc = RPN_Evaluator()
calc.eval('2 2 +')
calc.eval('1 2 3 4 * * *')
calc.eval('1 2 + 3 4 + 5 + +')
calc.eval('5 5 1 + * 2 /')
print calc.result()   # [4, 24, 15, 15]
