__author__ = 'Sunjoong LEE <sunjoong@gmail.com>'
__date__ = '2006-06-20'
__version__ = '1.0.0'

from new import function as mkfunction


def extractFunction(func, name = None):
    """Extract a nested function and make a new one.

    Example1>> def func(arg1, arg2):
                   def sub_func(x, y):
                       if x > 10:
                           return (x < y)
                       else:
                           return (x > y)

                   if sub_func(arg1, arg2):
                       return arg1
                   else:
                       return arg2


               func1 = extractFunction(func, 'sub_func')
               assert(func1(20, 15) == True)


    Example2>> class CL:
                   def __init__(self):
                       pass

                   def cmp(self, x, y):
                       return cmp(x, y)


               cmp1 = extractFunction(Cl.cmp)
    """
    if name == None and repr(type(func)) == "<type 'instancemethod'>":
        new_func = mkfunction(func.func_code, func.func_globals)
        return new_func

    if not hasattr(func, 'func_code'):
        raise ValueError, '%s is not a function.' % func

    code_object = None
    for const in func.func_code.co_consts.__iter__():
        if hasattr(const, 'co_name') and const.co_name == name:
            code_object = const

    if code_object:
        new_func = mkfunction(code_object, func.func_globals)
        return new_func
    else:
        raise ValueError, '%s does not have %s.' % (func, name)
