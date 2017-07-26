class C:
   def __init__(self, methodNames):
      for name in methodNames:
         setattr(C, name, self.methodClosure(name))
   def methodClosure(self, name):
      def method(*args, **kwargs):
         print name, args, kwargs
      return method

# test code
if __name__ == "__main__":
   c = C(['m1'])
   print hasattr(c,'m1')
   print hasattr(c,'m2')
   c.m1(0, a=10)
   c.m2(0, a=10)


# output of test code:
# True
# False
# m1 (<__main__.C instance at 0x12345678>, 0) {'a': 10}
# Traceback (most recent call last):
#   File "test.py", line 16, in ?
#     c.m2(0, a=10)
# AttributeError: C instance has no attribute 'm2'
