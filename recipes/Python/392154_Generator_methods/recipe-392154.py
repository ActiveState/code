#gendec.py

import weakref

class MethodGeneratorProxy(object):
  '''
  Wraps a generator method in a callable. On each call to an instance of this
  class, one of the following occurs: the generator advances one iteration and
  its result is returned, the generator is reset and None is returned, or the
  generator throws a StopIteration (which is caught) and None is returned.
  The generator is automatically re-instantiated on the next call after the
  StopIteraction exception is raised.

  This class does not maintain a strong reference to the object to which the
  method is attached. It will not impede garbage collection.

  @ivar func: Method that, when called, instantiates a generator
  @type func: function
  @ivar gen: Instantiated generator
  @type gen: generator
  @ivar reset_flag: Param to look for in keyword args as the signal to reset
  @type reset_flag: string
  '''     
  def __init__(self, func, reset_flag):
    '''
    Initializes an instance.

    See instance variables for parameter descriptions.
    '''       
    self.func = func
    self.gen = None
    self.reset_flag = reset_flag

  def __call__(self, obj, *args, **kwargs):
    '''
    Generate the next item or reset the generator.

    @param obj: Object to which the generator is attached
    @type obj: object
    @param args: Positional arguments to the generator method
    @type args: list
    @param kwargs: Keyword arguments to the generator method
    @type kwargs: dictionary
    '''       
    if kwargs.get(self.reset_flag):
      # reset the generator and return None
      self.gen = None
      return None
    elif self.gen is None:
      # create a new generator
      try:
        wobj = weakref.proxy(obj)
      except TypeError:
        wobj = obj
      self.gen = self.func(wobj, *args, **kwargs)

    try:
      # generate next item
      return self.gen.next()
    except StopIteration:
      # destroy the generator and return None
      self.gen = None
      return None

def generator_method(cls_name, reset_flag='reset_gen'):
  '''
  Decorator for methods that act as generators. Methods decorated as such can
  be called like normal methods, but can (and should) include yield statements.
  The parameters passed to the first invocation of the method are used for all
  subsequent calls until the generator is reset.

  Generator methods can be overriden in subclasses as long as the name provided
  is unique to each class in the inheritence tree (i.e. make it the name of the
  class and everything will work fine.

  To reset a generator method, pass True in a keyword argument with the name
  specified in reset_flag. Generator methods in parent classes must be reset
  explicitly (i.e. Parent.MethodName(self, reset_gen=True).

  @param cls_name: Name unique to the inheritence tree of this class
  @type cls_name: string
  @param reset_flag: Name of a parameter that will reset the generator
  @type reset_flag: string
  '''     
  # define another function that takes just the function as an argument
  # we must do this to deal with the fact that we need the name argument above
  def generator_method_internal(func):
    # build a name for the method generator
    name = '_%s_%s_gen_proxy_' % (cls_name, func.func_name)
    # define a replacement for a method that calls the generator instead
    def generator_method_invoke(obj, *args, **kwargs):
      try:
        # try to get a generator defined for the called method
        gen = getattr(obj, name)
      except AttributeError:
        # build a new generator for the called method
        gen = MethodGeneratorProxy(func, reset_flag)
        setattr(obj, name, gen)
      # call the generator and return its result
      return gen(obj, *args, **kwargs)
    # return our wrapping for the method
    return generator_method_invoke
  # return the true decorator for the method
  return generator_method_internal



# test.py
from gendec import generator_method

class Test(object):
  def __del__(self):
    print '* Test instance freed'

  def Reset(self):
    self.GetWords(reset_gen=True)

  @generator_method('Test')
  def GetWords(self):
    yield 'the quick'
    yield 'brown fox'
    yield 'jumped over'
    yield 'the lazy'
    yield 'dog'

class Foo(Test):
  def __del__(self):
    print '* Foo instance freed'

  def ResetAll(self):
    super(Foo, self).GetWords(reset_gen=True)
    self.GetWords(reset_gen=True)

  @generator_method('Foo')
  def GetWords(self):
    i = 0
    while 1:
      i += 1
      s = super(Foo, self).GetWords()
      yield '<%d> %s' % (i,s)

print '*** Test instance ***'
t = Test()
for i in range(8):
  print t.GetWords()
print '*** Resetting'
t.Reset()
for i in range(3):
  print t.GetWords()

print
print '*** Test instance #2 ***'
s = Test()
for i in range(3):
  print s.GetWords()

print
print '*** Foo subclass instance ***'
f = Foo()
for i in range(8):
  print f.GetWords()
print '*** Resetting Foo method only'
f.Reset()
for i in range(5):
  print f.GetWords()
print '*** Resetting Foo and Test methods'
f.ResetAll()
for i in range(3):
  print f.GetWords()
print
