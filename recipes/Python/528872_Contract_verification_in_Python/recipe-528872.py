import zope.interface.verify

def contractVerifier(implementer):
   for iface in list(implementer.__implemented__):
      implementer_name = implementer.__name__
      try:
         if zope.interface.verify.verifyClass(iface, implementer):
            print "OK: %s correctly implements %s" % (implementer_name, iface.__name__)
       except Exception, err:
           print "Error detected with %s's implementation: %s" % (implementer_name, err)

class IFoo(zope.interface.Interface):
   def foo(arg1): pass
   def bar(): pass # self is not reqd as Interfaces document how obj is used 

class Foo(object):
   zope.interface.implements(IFoo)
   def foo(self): pass

class Foo2(object):
   zope.interface.implements(IFoo)
   def foo(self, arg1): pass

class Foo3(object):
   zope.interface.implements(IFoo)
   def foo(self, arg1): pass
   def bar(self): pass

contractVerifier(Foo)
contractVerifier(Foo2)
contractVerifier(Foo3)
