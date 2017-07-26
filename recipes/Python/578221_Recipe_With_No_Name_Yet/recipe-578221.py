#!/usr/bin/python
# -*- coding: utf-8 -*-

# Recipe
# ----------------------------------------------------------------------------

class recipe:
    @staticmethod
    def enter_event(notified_f):
        def wrapper(f):
            def caller(obj, *args, **kargs):
                notified_f(obj, *args, **kargs)
                ret = f(obj, *args, **kargs)
                return ret
            return caller
        return wrapper
    
    @staticmethod
    def exit_event(notified_f):
        def wrapper(f):
            def caller(obj, *args, **kargs):
                # Start of diff between enter_event
                ret = f(obj, *args, **kargs)
                notified_f(obj, *args, **kargs)
                # End of diff between enter_event
                return ret
            return caller
        return wrapper

# Tests
# ----------------------------------------------------------------------------

class c:
    def notify_entering(self, *args, **kargs):
        print '  - function notify_entering() is triggered :'
        print '    - self  : [%s]' % self
        print '    - args  : %s' % repr(args)
        print '    - kargs : %s' % repr(kargs)
        print
    
    def notify_exiting(self, *args, **kargs):
        print '  - function notify_exiting() is triggered :'
        print '    - self : [%s]' % self
        print '    - args  : %s' % repr(args)
        print '    - kargs : %s' % repr(kargs)
        print
    
    # Method
    @recipe.enter_event(notify_entering)
    @recipe.exit_event(notify_exiting)
    def f(self, x):
        print '  - inside o.f() ...'
        print '    - self = [%s]' % self
        print '    - x = [%s]' % x
        print
    
    # Class method
    @classmethod
    @recipe.enter_event(notify_entering)
    @recipe.exit_event(notify_exiting)
    def fclass(cls, x):
        print '  - inside o.fclass() ...'
        print '    - cls = [%s]' % cls
        print '    - x = [%s]' % x
        print
    
    # Static method
    @staticmethod
    @recipe.enter_event(notify_entering)
    @recipe.exit_event(notify_exiting)
    def fstatic(x):
        print '  - inside o.fstatic() ...'
        print '    - x = [%s]' % x
        print

if __name__ == '__main__':
    o = c()

    print '-' * 78
    print '- calling o.f(123) ...'
    o.f(123)
    
    print '-' * 78
    print '- calling o.fclass(234) ...'
    o.fclass(234)
    
    print '-' * 78
    print '- calling o.fstatic(345) ...'
    o.fstatic(345)
