### The suggested superclass ###
class AutoInit (object) :
  """
  Each class that inherits from AutoInit (directly or indirectly) can
  specify all standard attributes and their initials in dictionary called
  classinitials.
  Important: if used, it is recommended to specify an attribute with default value None (for copy constructor)
  """

  def get_initials(self):
    # list of classes in inheritance list (superclasses first)
    # care should be taken with multiple inheritance, 
    # if unsure of class heirachy then overide all initials in originating class.
    clss = list(self.__class__.__mro__)
    clss.reverse()
    initials = {}
    for cls in clss:
      if hasattr(cls,'classinitials'):
        initials.update(getattr(cls,'classinitials'))
    return initials
  initials = property( get_initials )

  def __init__(self, *args, **kwargs) :
    # check that the class-attribute 'classinitials' exists
    if not hasattr(self, 'initials') : return
    # if arg is same type as this then copy construct
    if len(args) > 0 and self.__class__ == args[0].__class__ :
      arg = args[0] # first element in args is now object to copy
      # for each attribute in classinitials copy from arg.attribute to this.attribute
      for attribute in self.initials :
        setattr(self, attribute, getattr(arg, attribute))
    # where args is empty or first arg is not of same class then ignore.
    # insted copy all present managed attributes from kwargs dictionary
    # where not present get default from initials dictionary.
    else :
      for attribute in self.initials :
        if attribute in kwargs :
          setattr(self, attribute, kwargs[attribute])
        else :
          setattr(self, attribute, self.initials[attribute])

  def get_managed_dict(self):
    """
    Returns a dictionary of objects attributes, where attribute names are given in self.initials
    """
    return dict([ (k,getattr(self,k)) for k in self.initials ])
  
  def __str__(self):
    return str(self.get_managed_dict())


### example subclasses ###
class A(AutoInit):
  classinitials = { 'attr1' : 'set from A' }
  def __init__(self,*args,**kwargs):
    AutoInit.__init__(self,*args,**kwargs)

class B(A):
  classinitials = { 'attr2' : 'set from B' }
  def __init__(self,*args,**kwargs):
    A.__init__(self,*args,**kwargs)

class C(B):
  classinitials = {  'attr1' : 'set from C',
                  'attr3' : 'set from C' }
  def __init__(self,*args,**kwargs):
    B.__init__(self,*args,**kwargs)

### example usage ###
def test():
  a = A()
  b = B()
  c1 = C()
  c2 = C(attr1='set by constructor argument to c2')
  c3 = C(c2)
  print "Initialised objects:"
  print "a:",a
  print "b:",b
  print "c1:",c1
  print "c2:",c2
  print "c3:",c3
  print


  ## objects can then be used normally ##
  c1.attr1 = 'set externally'
  print "After manual set operation:"
  print "c1:",c1


### run from command line if you like ###
if __name__ == '__main__':
  test()
