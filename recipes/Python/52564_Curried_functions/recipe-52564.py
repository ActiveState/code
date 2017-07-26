CO_VARARGS = 0x0004
CO_VARKEYWORDS = 0x0008

class Curry:
   def __init__(self, f):
       self.hasv = f.func_code.co_flags & CO_VARARGS
       self.hask = f.func_code.co_flags & CO_VARKEYWORDS
       self.defaults = f.func_defaults or ()
       self.defnum = len(self.defaults)
       self.f = f
       self.argnum = f.func_code.co_argcount
       self._reset()
   def __call__(self, *a, **k):
       if k and not self.hask:
          raise TypeError, "%s got unexpected keyword argument '%s'" %\ 
                   (self.f.__name__, k.popitem()[0])
       kargs = self.kargs
       args = self.args
       kargs.update(k)
       totlen = len(args) + len(a)
       if totlen > self.argnum:
          if not self.hasv:
             raise TypeError, "%s takes exactly %d argument%c (%d given)" %                (self.f.__name__, self.argnum, ['s',''][self.argnum==1], totlen)
          args += a
          self._reset()
          return self.f(*args, **kargs)
       if totlen >= self.argnum - self.defnum:
          num_defaults = totlen - defnum
          args += a + self.defaults[defnum-num_defaults:]
          self._reset()
          return self.f(*args, **kargs)
       self.args += a
       return self
   def _reset(self):
       self.args, self.kargs = (), {}
