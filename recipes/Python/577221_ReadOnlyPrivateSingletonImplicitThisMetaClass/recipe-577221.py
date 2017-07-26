import sys
import inspect
import textwrap
import collections

class PrivateImplicitThisSingleton(type):

    def __new__(metaclass, name, bases, attrs):
        noop = lambda *args, **kwargs: None
        func_type = type(noop)
        private = {'object': None}
        class Context(collections.MutableMapping, dict):
            def __init__(self):
                self.globals = globals()
            def __delitem__(self, key):
                del self.globals[key]
            def __getitem__(self, key):
                return self.globals[key]
            def __setitem__(self, key, val):
                self.globals[key] = val
        context = Context()
        for func_name, old_func in attrs.iteritems():
            if isinstance(old_func, func_type):
                try:
                    save = context[func_name]
                    restore = True
                except KeyError:
                    restore = False
                exec textwrap.dedent(inspect.getsource(old_func)).replace('(', '(this,', 1) in context
                attrs[func_name] = context[func_name]
                if restore:
                    context[func_name] = save
                else:
                    del context[func_name]
        def new_object(cls, *args, **kwargs):
            if private['object'] is None:
                private['object'] = bases[0].__new__(cls)
                private['object'].__init__(*args, **kwargs)
                cls.__init__ = noop
                private['attrs'] = private['object'].__dict__
                del private['object'].__dict__
                def check_access():
                    if sys._getframe(2).f_globals is not context:
                        raise AttributeError('private')
                def get_attr(self, key):
                    try:
                        val = private['attrs'][key]
                        check_access()
                        return val
                    except KeyError:
                        return super(cls, self).__getattribute__(key)
                def set_attr(self, key, val):
                    check_access()
                    private['attrs'][key] = val
                cls.__getattribute__ = get_attr
                cls.__setattr__ = set_attr
            return private['object']
        attrs['__new__'] = new_object
        return type(name, bases, attrs)


class RockStarEnterpriseClass(object):

    __metaclass__ = PrivateImplicitThisSingleton

    def __init__(val):
        this.val = val

    def getVal():
        return this.val

    def setVal(val):
        this.val = val
