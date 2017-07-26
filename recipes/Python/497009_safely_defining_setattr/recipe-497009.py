class MyClass(object):
  def __init__(self, foo, bar):
    # set attributes normally here
    self.foo = foo
    self.bar = bar

    # override __setattr__
    # NOTE: doesn't really work, __setattr_impl won't be called.
    self.__setattr__ = self.__setattr_impl

  def __setattr_impl(self, name, value):
    pass # definition goes here
