from sets import Set, ImmutableSet
from types import TypeType, ClassType, NoneType, InstanceType


class Error(ValueError):
   """Error class for Watchdog"""

   def __init__(self, func, value, exp_type, name, number = None):
      try:
         prefix = "value '%s' of " % value
      except:
         prefix = ''
      if number != None:
         number_str = ' #%s' % number
      else:
         number_str = ''
      msg = "mismatch in file '%s', line %s: %s%s%s should be %s, got %s" % (
            func.func_code.co_filename, func.func_code.co_firstlineno,
            prefix, name, number_str, exp_type, type(value))
      ValueError.__init__(self, msg)


class Watchdog(object):

   # cache for parameters / result types:
   signatures = Set()

   def __new__(cls, para_types, res_type, strict = False):
      if not strict and not __debug__:
         # decorator: identity, does nothing
         return lambda func: func
      # create watchdog instance:
      watchdog = object.__new__(cls)
      # assign function signature to instance & add to cache if needed:
      signature = para_types, res_type
      if signature not in Watchdog.signatures:
         # unknown signature: check and insert
         if not isinstance(para_types, tuple):
            raise ValueError('Parameter #1 must be a tuple')
         allow_types = [TypeType, ClassType]
         for entry in para_types:
            if type(entry) not in allow_types:
               msg = 'Parameter #1 must contain only Types and/or Classes'
               raise ValueError(msg)
         if type(res_type) not in allow_types:
            raise ValueError('Parameter #2 must be a Type or Class')
         Watchdog.signatures |= ImmutableSet([signature])
      watchdog.signature = signature
      # returns the decorator(not the watchdog class-instance):
      return watchdog.check


   def check(self, func):

      def caller(*args):
         # load function signature:
         para_types, res_type = self.signature
         normal_len = func.func_code.co_argcount
         submit_len = len(args)
         if normal_len != len(para_types):
            raise ValueError('wrong number of parameter types')
         # check if there are conflicts with user arguments:
         pairs = zip(args, para_types, range(1, submit_len + 1))
         for pair in pairs:
            if not isinstance(pair[0], pair[1]):
               raise Error(func, pair[0], pair[1], 'parameter', pair[2])
         try:
            # check default parameter integrity:
            default_args = func.func_defaults
            default_len = len(default_args)
            default_types = para_types[0: default_len]
            count_range = range(normal_len - default_len + 1, normal_len + 1)
            pairs = zip(default_args, default_types, count_range)
            for pair in pairs:
               if not isinstance(pair[0], pair[1]):
                  raise Error(func, pair[0], pair[1],
                              'default parameter', pair[2])
         except TypeError:
            # no default arguments: ignore
            pass
         # we actually call the function here:
         res = func(*args)
         # check result integrity:
         if not isinstance(res, res_type):
            raise Error(func, res, res_type, 'result')
         return res
 
      return caller



if __name__ == "__main__":

   # a small test:
   # try to run "python watchdog.py" and "python -O watchdog.py"

   @Watchdog((int, int), int, strict = True)
   def add(a, b):
      return a + b

   @Watchdog((int, int), int) # strict is implicitly set to False
   def sub(a, b):
      return a - b

   # strict checking(not affected by __debug__):
   try:
      add(1, '3')
   except Error, err:
      print 'strict check failed: %s' % err

   # non-strict checking(affected by __debug__):
   try:
      sub([1,2,3], 7)
   except Error, err:
      print 'non-strict check failed: %s' % err
