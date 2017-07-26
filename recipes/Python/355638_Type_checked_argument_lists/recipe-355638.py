def require(*types):
    '''
    Return a decorator function that requires specified types.
    types -- tuple each element of which is a type or class or a tuple of
             several types or classes.
    Example to require a string then a numeric argument
    @require(str, (int, long, float))

    will do the trick
    '''
    def deco(func):
        '''
        Decorator function to be returned from require().  Returns a function
        wrapper that validates argument types.
        '''
        def wrapper (*args):
            '''
            Function wrapper that checks argument types.
            '''
            assert len(args) == len(types), 'Wrong number of arguments.'
            for a, t in zip(args, types):
                if type(t) == type(()):
                    # any of these types are ok
                    assert sum(isinstance(a, tp) for tp in t) > 0, '''\
%s is not a valid type.  Valid types:
%s
''' % (a, '\n'.join(str(x) for x in t))
                assert isinstance(a, t), '%s is not a %s type' % (a, t)
            return func(*args)
        return wrapper
    return deco

@require(int)
def inter(int_val):
    print 'int_val is ', int_val

@require(float)
def floater(f_val):
    print 'f_val is ', f_val

@require(str, (int, long, float))
def nameAge1(name, age):
    print '%s is %s years old' % (name, age)

# another way to do the same thing
number = (int, float, long)
@require(str, number)
def nameAge2(name, age):
    print '%s is %s years old' % (name, age)

nameAge1('Emily', 8)       # str, int ok
nameAge1('Elizabeth', 4.5) # str, float ok
nameAge2('Romita', 9L)     # str, long ok
nameAge2('Emily', 'eight') # raises an exception!
