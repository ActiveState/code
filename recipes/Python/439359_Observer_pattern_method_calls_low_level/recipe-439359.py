import types,itertools,weakref,sets,random
generatorTypes=(type(itertools.chain()),types.GeneratorType) # a bug?

###################   decorators section ###################
def hook(**kwargs):
  default=dict(obserstack=False,external=False,hooks=(),fired=True,after=True,success=1.)
  default.update(kwargs)
  class meta:
    locals().update(default)
  def wrapper(func):
    func.metaObser=meta
    return func
  return wrapper
def hookable(function):
  return hook()(function)
def firedAfter(*observed,**kwargs):
  kwargs.update(hooks=observed)
  return hook(**kwargs)
def triggerAfter(*observers,**kwargs):
  kwargs.update(hooks=observers,fired=False)
  return hook(**kwargs)
def firedBefore(*observed,**kwargs):
  kwargs.update(hooks=observed,after=False)
  return hook(**kwargs)
def triggerBefore(*observers,**kwargs):
  kwargs.update(hooks=observed,fired=False,after=False)
  return hook(**kwargs)

class Wrapper(object):
  ''' A descriptor to call the hooks around the function .
  As this need to know the klass ,it must be instantiated from metaclasses.
  Name is the method name, so (klass,name) is the key to refer to callbacks
  '''
  def __init__(self,klass,function,name):
    self.klass=klass
    self.function=function
    self.name=name 
    self.obserstack=function.metaObser.obserstack
  def __get__(self,object,*_):  
    def wrapper(*args,**kwargs):
      stack=kwargs.pop('obserstack',[])[:]
      stack.append((object,self.klass,self.name))
      kwargs['obserstack']=stack
      
      chain=[]      
      def chainIfCase(result):
        if type(result) in generatorTypes:
          chain.append(result)
          return True
        return False
       
      def caller(instance,name):
        chainIfCase(getattr(instance,name)(*args,**kwargs))

      def execHooks(external,after):
        for (kls,name),success in self.klass.hooks[after,external].get(self.name,()): 
          if external:
            for instance in kls.instances:
              if random.random()<success:
                caller(instance,name)
          else:
            if isinstance(object,kls) and random.random()<success:
              caller(object,name)
      
      for external in (True,False):
        execHooks(external,after=False)
      
      if not self.obserstack:
        del kwargs['obserstack']
      result=self.function(object,*args,**kwargs)
      generator=chainIfCase(result)
      if not self.obserstack:
        kwargs['obserstack']=stack
      
      for external in (False,True):
        execHooks(external,after=True)
        
      if generator:
        return itertools.chain(*chain)  
      return result
      
    wrapper.klass=self.klass # avoiding a dictionary to record this
    wrapper.__name__=self.name # debugging help
    return wrapper
    
class Instances(object):
  def __get__(self,cls,_):
    instances=set(_() for _ in cls.classInstances)
    for derived in cls.deriveds:
      instances|=derived.instances
    return instances
  def __set__(self,cls,instance):
    cls.classInstances.add(weakref.ref(instance,cls.classInstances.remove))

class Hooks(object):
  def __init__(self):
    self.hooks=(({},{}),({},{}))
  def __getitem__(self,(after,external)):
    return self.hooks[after][external]
     
class MetaObsers(type):
  instances=Instances() # instances resolver
  def __init__(cls,_,bases,__):
    for base in bases: # update superclasses
      if hasattr(base,'deriveds'):
        base.deriveds.add(cls)
    cls.hooks=Hooks() # hooks initializations
    cls.deriveds=set() # the ipoclasses register
    cls.classInstances=set() # this weakref register of this class instances
    for name in dir(cls): # the decorated function wrapping
      attribute=getattr(cls,name)
      if hasattr(attribute,'im_func') and hasattr(attribute.im_func,'metaObser'):
        cls.wrap(attribute.im_func,name) 
  def wrap(cls,function,name): 
    ''' A method to add new wrapped functions to the classes.'''
    if not hasattr(function,'metaObser'):
      raise TypeError('function %s has no "metaObser" attribute'%str(function))
    meta=function.metaObser
    setattr(cls,name,Wrapper(cls,function,name))
    for obser in meta.hooks:
      if not hasattr(obser,'klass'):# checks on targets validity
        raise TypeError('The obser %s has no "klass" attribute'%str(obser))
      if not Obser in obser.klass.__mro__: # not pythonic
        raise TypeError('The target method class %s of method %s was  not derived from Obser'%(str(obser.klass),obser.__name__))
      if meta.fired:
        obser.klass.hooks[meta.after,meta.external].setdefault(obser.__name__,[]).append(((cls,name),meta.success))
      else:
        cls.hooks[meta.after,meta.external].setdefault(name,[]).append(((obser.klass,obser.__name__),meta.success))
  def __str__(cls):
    return str(cls.__module__)+cls.__name__
    
class Obser(object):
  ''' Base class for observables.'''
  __metaclass__=MetaObsers
  def __init__(self,*args,**kwargs): #to be called :)
    super(Obser,self).__init__(*args,**kwargs)
    self.__class__.instances=self
  #defaults
  def __hash__(self):
    return id(self)
  def __str__(self):
    return str(id(self))
