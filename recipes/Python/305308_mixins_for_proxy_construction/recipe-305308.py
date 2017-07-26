#=======================================================================

__version__ = '''0.1.01'''
__sub_version__ = '''20040919004511'''
__copyright__ = '''(c) Alex A. Naanou 2003'''


#-----------------------------------------------------------------------

__doc__ = '''\
this module will define a set of utilities and classes to be used to build
various proxies...
'''


#-----------------------------------------------------------------------

import new
import types
import weakref


#-----------------------------------------------------------------------
#------------------------------------------------------getproxytarget---
def getproxytarget(obj):
    '''
    this will return the unproxied target object.
    '''
    ogetattribute = object.__getattribute__
    try:
        return ogetattribute(obj, ogetattribute(obj, '__proxy_target_attr_name__'))
    except:
        if not isproxy(obj):
            raise TypeError, 'obj must be a proxy (got: %s).' % obj
        raise


#-------------------------------------------------------------isproxy---
def isproxy(obj):
    '''
    this will return True if obj is a proxy object (relative to AbstractProxy).

    NOTE: this will work only for the pli framework proxies that inherit 
          from AbstractProxy.
    '''
    return isinstance(obj, AbstractProxy)



#-----------------------------------------------------------------------
#-------------------------------------------------------AbstractProxy---
# this is here for:
#   1) use of isproxy.
#      it is helpful if all *similar* classes be a subclass of one
#      parent class for easy identification...
#   2) define the default configuration for use with the 'proxymethod'
#      and helper functions...
class AbstractProxy(object):
    '''
    this is a base class for all proxies...
    '''
    __proxy_target_attr_name__ = 'proxy_target'


#----------------------------------------------------------BasicProxy---
class BasicProxy(AbstractProxy):
    '''
    this defines a nice proxy repr mixin.
    '''
    def __repr__(self):
        '''
        '''
        ogetattribute = object.__getattribute__
        return '<%s proxy at %s to %s>' % (ogetattribute(self, '__class__').__name__, 
                                            hex(id(self)),
                                            repr(getproxytarget(self)))



#-----------------------------------------------------------------------
# this section defines component mix-ins...
#-----------------------------------------------------ComparibleProxy---
class ComparibleProxy(BasicProxy):
    '''
    proxy mixin. this will transfer the rich comparison calls directly 
    to the target...
    '''
    __proxy_target_attr_name__ = 'proxy_target'

    # these cant be avoided without eval...
    def __eq__(self, other):
        return getproxytarget(self) == other    
    def __ne__(self, other):
        return getproxytarget(self) != other
    def __gt__(self, other):
        return getproxytarget(self) > other 
    def __lt__(self, other):
        return getproxytarget(self) < other 
    def __ge__(self, other):
        return getproxytarget(self) >= other    
    def __le__(self, other):
        return getproxytarget(self) <= other    


#---------------------------------------------------------CachedProxy---
# NOTE: from here on all proxies are by default cached...
class CachedProxy(BasicProxy):
    '''
    this defaines the basic proxy cache manager functionality.
    '''
    # this may either be None or a dict-like (usualy a weakref.WeakKeyDictionary)
    # if None the proxy caching will be disabled
    __proxy_cache__ = None

    def __new__(cls, source, *p, **n):
        '''
        return the cached proxy or create a one and add it to cache.
        '''
        res = cls._getcached(source)
        if res == None and hasattr(cls, '__proxy_cache__') \
                and cls.__proxy_cache__ != None:
            obj = super(CachedProxy, cls).__new__(cls, source, *p, **n)
            cls._setcache(source, obj)
            return obj
        return super(CachedProxy, cls).__new__(cls, source, *p, **n)
    @classmethod
    def _getcached(cls, source):
        '''
        get an object from cache.
        if the object is not in cache or cache is disabled None will be returned.
        '''
        if hasattr(cls, '__proxy_cache__') and cls.__proxy_cache__ != None \
                and source in cls.__proxy_cache__:
            return cls.__proxy_cache__[source]
        return None
    @classmethod
    def _setcache(cls, source, obj):
        '''
        add an object to cache.
        '''
        if hasattr(cls, '__proxy_cache__') and cls.__proxy_cache__ != None:
            cls.__proxy_cache__[source] = obj

        

#-----------------------------------------------------------------------
# this section defines ready to use base proxies...
#---------------------------------------------InheritAndOverrideProxy---
# this is the Proxy cache...
_InheritAndOverrideProxy_cache = weakref.WeakKeyDictionary()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# this works as follows:
# 1) create a class that inherits from InheritAndOverrideProxy and the
#    proxied objects class...
#    reference code:
#       class local_proxy(InheritAndOverrideProxy, proxied.__class__):
#           pass
# 2) creates an object from the above class, and sets its __dict__ to
#    reference the target objects __dict__. thus enabling setting and
#    referencing data to the proxied object....
#
class InheritAndOverrideProxy(CachedProxy):
    '''
    this is a general (semi-transparent) proxy.
    '''
    # this defines the attribute name where the proxy target is
    # stored...
    __proxy_target_attr_name__ = 'proxy_target'
    # this is used to generate unique proxy class names...
    __proxy_count__ = 0
    # this may either be None or a dict-like (usualy a weakref.WeakKeyDictionary)
    # if None the proxy caching will be disabled
    __proxy_cache__ = _InheritAndOverrideProxy_cache

    def __new__(cls, source, *p, **n):
        '''
        this will create a proxy, wrap the target and return the result... 
        else return the target.
        '''
        osetattr = object.__setattr__
        cls_name = cls.__name__
        try:
            # process proxy cache...
            _obj = cls._getcached(source)
            if _obj != None:
                return _obj
            # create an object of a class (also just created) inherited
            # from cls and source.__class__
            _obj = object.__new__(new.classobj('',(cls, source.__class__), {}))
            # get the new class....
            cls = object.__getattribute__(_obj, '__class__')
            # name the new class... 
            # NOTE: the name may not be unique!
            cls.__name__ = cls_name + '_' + str(cls.__proxy_count__)
            cls.__proxy_count__ += 1
            # considering that the class we just created is unique we
            # can use it as a data store... (and we do not want to
            # pollute the targets dict :) )
            setattr(cls, cls.__proxy_target_attr_name__, source)
            # replace the dict so that the proxy behaves exactly like
            # the target...
            osetattr(_obj, '__dict__', source.__dict__)
        # we fall here in case we either are a class constructor, function or a callable....
        # WARNING: this might be Python implementation specific!!
        except (TypeError, AttributeError), e:
            # function or callable
            if type(source) in (types.FunctionType, types.LambdaType, \
                                    types.MethodType, weakref.CallableProxyType):
                # callable wrapper hook...
                if hasattr(cls, '__proxy_call__') and cls.__proxy_call__ != None:
                    return cls.__proxy_call__(source)
                return source
            # class (nested class constructors...)
            elif callable(source):
                # class wrapper hook...
                if hasattr(cls, '__proxy_class__') and cls.__proxy_class__ != None:
                    return cls.__proxy_class__(source)
                return source
            return source
        # process proxy cache...
        cls._setcache(source, _obj)
        return _obj
    # this is here to define the minimal __init__ format...
    # WARNING: there is a danger to call the targets __init__ so
    #          keep this empty!!!
    def __init__(self, source, *p, **n):
        pass
    # these two methods are the optional function and class wrappers...
##  def __proxy_call__(self, target):
##      return target
##  def __proxy_class__(self, target):
##      return target


#-----------------------------------TranparentInheritAndOverrideProxy---
# this is the Proxy cache...
_TranparentInheritAndOverrideProxy_cache = weakref.WeakKeyDictionary() 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TranparentInheritAndOverrideProxy(InheritAndOverrideProxy, ComparibleProxy):
    '''
    this is a transparent variant of InheritAndOverrideProxy. its' behavior 
    is in no way different from the proxied object.

    NOTE: due to the fact that this explicitly proxies the __getattribute__ 
          and __setattr__ calls, it is slower then the semi-transparent 
          variant.
    '''
    __proxy_target_attr_name__ = 'proxy_target'
    __proxy_count__ = 0
    __proxy_cache__ = _TranparentInheritAndOverrideProxy_cache
    # this defines the attributes that are resolved to the proxy itself
    # (not the target object)...
    __proxy_public_attrs__ = (
                '__proxy_call__',
                '__proxy_class__',
            )

    def __getattribute__(self, name):
        '''
        '''
        ogetattribute = object.__getattribute__
        if name in ogetattribute(self, '__proxy_public_attrs__') \
                + (ogetattribute(self, '__proxy_target_attr_name__'),):
            return super(TranparentInheritAndOverrideProxy, self).__getattribute__(name)
        return self.proxy_target.__getattribute__(name)



#=======================================================================
if __name__ == '__main__':
    # Examples:
    #
    # here we create a class we will use as a target for our proxy...
    # this will define same special methods, normal methods and
    # attributes (both class and object)...
    class O(object):
        class_attr = 'some value...'
        def __init__(self):
            self.obj_attr = 1234567
        def __call__(self):
            print 'O object (__call__)! (', self.__class__, hex(id(self)), ').'
        def meth(self, arg):
            print 'O object (meth)! (', self.__class__, hex(id(self)), ').'
    # create an instance of the above...
    o = O()
    # now the fun starts..
    # we define a proxy that will intercept calls to the target object.
    class Proxy(TranparentInheritAndOverrideProxy):
        def __call__(self, *p, **n):
            print 'Proxy:\n\t',
            self.proxy_target(*p, **n)
    # bind a proxy to the target...
    p = Proxy(o)
    # call the original...
    o()
    # call the proxy...
    p()
    # raw access attributes...
    print p.obj_attr
    print p.class_attr
    # set attributes via the proxy...
    p.xxx = 'xxx value...'
    p.obj_attr = 7654321
    # access new values attributes...
    print o.xxx
    print o.obj_attr
    print o.class_attr
    # print the class of the proxy and the target...
    print 'o.__class__ is', o.__class__
    print 'p.__class__ is', p.__class__
    # compare the two...
    print 'o == p ->', o == p
    # isproxy tests...
    print 'p is a proxy test ->', isproxy(p)
    print 'o is a proxy test ->', isproxy(o)
    # print a nice repr...
    print 'o is', o
    print 'p is', p
    # now we test the cache...
    # create several proxies to the same object....
    p0 = Proxy(o)
    p1 = Proxy(o)
    # test if they are the same...
    print p is p0, p0 is p1



#=======================================================================
#                                   vim:set ts=4 sw=4 nowrap expandtab:
