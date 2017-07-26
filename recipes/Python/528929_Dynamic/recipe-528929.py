class Composer:
    '''
    The Composer class holds a list of higher order functions. It might b
    adapted in various ways.
    '''
    def __init__(self):
        self.callables = []        
                
def weave(composer):
    '''
    Basic layout for a decorator that composes functions hold independently
    in a Composer object. 
    '''
    def wrap(f):        
        def weaving(*args, **kwd):
            g = f
            for h in composer.callables:                
                g = h(g)            
            return g(*args, **kwd)
        weaving.__name__ = f.__name__            
        return weaving    
    return wrap

def composite(f):
    '''
    Used to turn an ordinary function into a higher order function being 
    composed with its argument. The composite function can be used as a 
    decorator. But that's not our use pattern here.
    '''
    def compose(g):
        def wrap(*args, **kwd):
            return f(g(*args, **kwd))
        wrap.__name__ = g.__name__
        return wrap
    compose.__name__ = f.__name__
    return compose


#
#
# Example
#
#

composer = Composer()

@weave(composer)
def foo(x):
    return x

def duplicate(x):
    if isinstance(x, list):
        return x+x
    else:
        return x

# check it out

>>> foo(1)
1
>>> composer.callables.append(composite(duplicate))
>>> foo(1)
[1,1]
>>> composer.callables.append(composite(duplicate))
>>> foo(1)
[1,1,1,1]
