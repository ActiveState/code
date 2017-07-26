import sys

class AutoIndent(object):
    def __init__(self, stream):
        self.stream = stream
        self.offset = 0
        self.frame_cache = {}

    def indent_level(self):
        i = 0
        base = sys._getframe(2)
        f = base.f_back
        while f:
            if id(f) in self.frame_cache:
                i += 1
            f = f.f_back
        if i == 0:
            # clear out the frame cache
            self.frame_cache = {id(base): True}
        else:
            self.frame_cache[id(base)] = True
        return i

    def write(self, stuff):
        indentation = '  ' * self.indent_level()
        def indent(l):
            if l:
                return indentation + l
            else:
                return l
        stuff = '\n'.join([indent(line) for line in stuff.split('\n')])
        self.stream.write(stuff)

--------------------------------------------------------------------------
>>> # Example usage 
>>>
>>> def f(x):
...     print "f(%s)" % x
...     if x == 0:
...         return 0
...     elif x == 1:
...         return 1
...     else:
...         return f(x-1) + f(x-2)
>>>
>>> import sys
>>> sys.stdout = AutoIndent(sys.stdout)
>>>
>>> f(6)
f(6)
  f(5)
    f(4)
      f(3)
        f(2)
          f(1)
          f(0)
        f(1)
      f(2)
        f(1)
        f(0)
    f(3)
      f(2)
        f(1)
        f(0)
      f(1)
  f(4)
    f(3)
      f(2)
        f(1)
        f(0)
      f(1)
    f(2)
      f(1)
      f(0)
8
>>>
