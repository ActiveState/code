#!/usr/bin/env python
# 
#   Copyright 2010-  Hui Zhang
#   E-mail: hui.zh012@gmail.com
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__all__ = ["Attribute", "attribute", ]

from weakref import ref
from functools import partial

class BaseAttribute(object):
    """        
        usage:
            >>>class A(object):
                   val = Attriubte('val',
                                 factory=int, 
                                 validator=lambda v: v in range(3,7),
                                 onchanged=somfunc, 
                                 readonly=True,
                                 otw=False,
                                 ...   # for more please check the code
                                 )
            >>> a = A()
            >>> print a.val
            0
            >>> a.val=1; print a.val
            1
            >>> del a.val; print a.val
            0
                          
            notes:
                'del a.val' does not delete the attr from instance.
                it just clean the assigned value for this attr. 

        parameters:
        
        * name :
            the attr's name, default is ''
        * readonly :
            define if the attr could be assigned.
            notes: readonly does not impact behavior of 'del a.val'
        * delable :
            define if the value could be deleted

        * default :
            the default value.
        * factory, boundfactory
            define the initializer for the attr.
            -factory takes no parametor 
            -boundfactory would get the instance as the only parameter.

        * validator, boundvalidator, skip_valid_err
            validate the value assigned to the attr.
            if validate failed,
                - the value would not be assigned
                - a exception would be raised if skip_valid_err is False.
            The validation would not be applied for the value initialized by: 
                default, factory, boundfactory
            
        * onchanged
            define a hook while attr value changed.
            the following 4 args would be given to the hook:
                (instance, Attribute instance, old value, new value)
                
        * otw
            one time write.
            e.g:
                class A(object):
                    v = Attribute(otw=True)
                    
                class B(A):
                    def __init__(self, value):
                        self.v = value
                        
                b = B(99)
                print b.v -> 99
                b.v = 100 -> exception raised

        [initialization:]
            initializers are prioritized as "default, factory, boundfactory"
            if no any defined and value assinged, a exception would be raised while you try to read this attr. 
        
    """
    undefined = object()
    
    def __init__(self, name='', **kwargs):
        self.name = name
        self.dict = kwargs.copy()
        
        self.skip_valid_err = self.getarg('skip_valid_err', True)
        
        self.build_initer()
        self.build_assigner()
        self.build_deleter()
        
        onchanged = self.getarg('onchanged', None)
        if onchanged:
            self.onchanged(onchanged)

    ## read, write and erase the value from/to the storage
    ## to be implemented by sub classes
    def _read_(self, instance):
        """ read the value from the storage
            raise exception if the value is not initialized 
        """

    def _write_(self, instance, value):
        """ store the value to the storage
        """
        
    def _earase_(self, instance):
        """ erase the value from the storage
        """
            
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            try:
                return self._read_(instance)
            except:
                if self.initer:
                    self._write_(instance, self.initer(instance))
                    return self._read_(instance)
                
                raise AttributeError("Attribute is used before initialized.")
    
    def __set__(self, instance, value):
        self.assigner(instance, value)
        
    def __delete__(self, instance):
        self.deleter(instance)

    ## build the initer, assigner and deleter
    def getarg(self, name, default):
        if name in self.dict:
            return self.dict.pop(name)
        else:
            return default
    
    def build_initer(self):
        self.initer = None
        
        _dummy = object
        
        default = self.getarg('default', _dummy)
        if default is not _dummy:
            self.initer = lambda instance: default
            return

        factory = self.getarg('factory', _dummy)
        if factory is not _dummy:
            self.initer = lambda instance: factory()
            return
        
        boundfactory = self.getarg('boundfactory', _dummy)
        if boundfactory is not _dummy:
            self.initer = lambda instance: boundfactory(instance)
            return
        
    def build_assigner(self):
        readonly = self.getarg('readonly', False)
        if readonly:
            def assigner(instance, value):
                raise AttributeError("Cannot set value to read-only attribute")
            self.assigner = assigner
            return
        
        self.assigner = self._write_
        
        otw = self.getarg('otw', False)
        if otw:
            self.set_otw()

        validator = self.getarg('validator', None)
        if validator:
            self.validator(validator)
        
        boundvalidator = self.getarg('boundvalidator', None)
        if boundvalidator:
            self.boundvalidator(boundvalidator)
    
    def build_deleter(self):
        delable = self.getarg('delable', True)
        if not delable:
            def deleter(instance):
                raise AttributeError("Cannot delete attribute")
            self.deleter = deleter
        else:
            self.deleter = self._earase_
    
    ## handler wrappers
    def set_otw(self):
        oldassinger = self.assigner
        def assigner(instance, value):
            try:
                self._read_(instance)
                inited = True
            except:
                inited = False
            if inited:
                raise AttributeError('Attribute could only be written once.')
            oldassinger(instance, value)
        self.assigner = assigner

    # be able to use as decorator
    def onchanged(self, hook):
        def wrap(func):
            def newfunc(*args):
                instance = args[0]
                try:
                    oldval = self.__get__(instance, None)
                except:
                    oldval = BaseAttribute.undefined
                    
                func(*args)
                
                try:
                    newval = self.__get__(instance, None)
                except:
                    newval = BaseAttribute.undefined
                
                if oldval != newval:
                    hook(instance, self, oldval, newval)
            return newfunc
        
        self.assigner = wrap(self.assigner)
        self.deleter = wrap(self.deleter)
        return self

    def validator(self, hook):
        oldassinger = self.assigner
        def assigner(instance, value):
            if hook(value):
                oldassinger(instance, value)
            elif not self.skip_valid_err:
                raise AttributeError("The value for attribute is not valid")
        self.assigner = assigner
        return self

    def boundvalidator(self, hook):
        oldassinger = self.assigner
        def assigner(instance, value):
            if hook(instance, value):
                oldassinger(instance, value)
            elif not self.skip_valid_err:
                raise AttributeError("The value for attribute is not valid")
        self.assigner = assigner
        return self

class Attribute(BaseAttribute):
    def __init__(self, name='', **kwargs):
        super(Attribute, self).__init__(name, **kwargs)
        self.__values = weakkeymap() # Recipe 577580: weak reference map 
        
    def _read_(self, instance):
        return self.__values.get(instance)
    
    def _write_(self, instance, value):
        self.__values.set(instance, value)
        
    def _earase_(self, instance):
        self.__values.remove(instance)

def attribute(*args, **kwargs):
    assert 'boundfactory' not in kwargs \
            and ( not args
                  or (len(args)==1 and not kwargs)
                 )
    
    if args:
        return Attribute(args[0].func_name, 
                         boundfactory=args[0])
    else:
        def deco(func):
            return Attribute(func.func_name,
                             boundfactory=func,
                             **kwargs)
        return deco
    
## demo code
#class A(object):
#    @attribute(skip_valid_err=False)
#    def value(self):
#        return 10000
#    
#    @value.boundvalidator
#    def value(self, v):
#        return v < 20
#
#    value.validator(lambda v: v>5)
#    
#    @value.onchanged
#    def value(self, *args):
#        print args
#    
#a = A()
#print a.value
#a.value = 9
#print a.value
#a.value = 100
