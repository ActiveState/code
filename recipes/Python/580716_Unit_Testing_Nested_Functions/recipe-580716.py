import types

def freeVar(val):
  def nested():
    return val
  return nested.__closure__[0]

codeAttribute = '__code__' if sys.version_info[0] == 3 else 'func_code'

def nested(outer, innerName, **freeVars):
  if isinstance(outer, (types.FunctionType, types.MethodType)):
    outer = outer.__getattribute__(codeAttribute)
  for const in outer.co_consts:
    if isinstance(const, types.CodeType) and const.co_name == innerName:
      return types.FunctionType(const, globals(), None, None, tuple(
          freeVar(freeVars[name]) for name in const.co_freevars))
