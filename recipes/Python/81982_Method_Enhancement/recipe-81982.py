from __future__ import nested_scopes
import new

def enhance_method(klass, method_name, replacement):
    'replace a method with an enhancement'
    method = getattr(klass, method_name)
    setattr(klass, method_name, new.instancemethod(
        lambda *args, **kwds: replacement(method, *args, **kwds), None, klass))

def method_logger(old_method, self, *args, **kwds):
    'enhancement that logs all calls to a method'
    print '*** calling: %s%s, kwds=%s' % (old_method.__name__, args, kwds)
    return_value = old_method(self, *args, **kwds) # call the original method
    print '*** %s returns: %s' % (old_method.__name__, `return_value`)
    return return_value

def demo():
    class Deli:
        def order_cheese(self, cheese_type):
            print 'Sorry, we are completely out of %s' % cheese_type

    d = Deli()
    d.order_cheese('Gouda')
    
    enhance_method(Deli, 'order_cheese', method_logger)
    d.order_cheese('Cheddar')
