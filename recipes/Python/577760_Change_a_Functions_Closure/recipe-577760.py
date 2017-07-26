"""inject_closure module"""

INJECTEDKEY = "injected_{}"
OUTERLINE = "    outer_{0} = injected_{0}"
INNERLINE = "        inner_{0} = outer_{0}"
SOURCE= ("def not_important():",
                 "    def also_not_important():",
                 "    return also_not_important")

def inject_closure(f, *args):
      """Return a copy of f, with a new closure.
      
      The new closure will be derived from args, in the same
      order.  This requires that the caller have knowledge
      of the existing closure.

      """

      # build the source to exec
      injected = {}
      source = list(SOURCE)
      for i in range(len(args)):
          source.insert(1, OUTERLINE.format(i))
          source.insert(-1, INNERLINE.format(i))
          injected[INJECTEDKEY.format(i)] = args[i]

      # exec the source and pull the new closure
      exec("\n".join(source), injected, injected)
      closure = injected["not_important"]().__closure__

      # build the new function object
      func = type(f)(f.__code__, f.__globals__, f.__name__,
                                 f.__defaults__, closure)
      func.__annotations__ = f.__annotations__
      func.__doc__ = f.__doc__
      func.__kwdefaults__ = f.__kwdefaults__
      func.__module__ = f.__module__

      return func
