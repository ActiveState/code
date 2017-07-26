"""Python implementation of PEP-380 (yield from)."""
from functools import wraps

class _from(object):
    """Wrap a generator function to be used from a supergenerator."""
    def __init__(self, genfunc):
        self.genfunc = genfunc

def supergenerator(genfunc):
    """
    Decorate a generator so it can yield nested generators (using _from class).
    
    @supergenerator
    def mysupergen():
        yield "normal yield"
        yield "one more yield"
        yield _from(othergen())
        yield _from(yet_othergen()) 
        yield "last yield"
    
    Note that nested generators can, in turn, yield other generators.    
    """
    def _process(gen):
        tosend = None
        while 1:
            yielded = gen.send(tosend)
            if isinstance(yielded, _from):
                nested_gen = _process(yielded.genfunc)
                nested_tosend = None
                while 1:
                    try:
                        nested_yielded = nested_gen.send(nested_tosend)
                    except StopIteration, exc:
                        new_tosend = (exc.args[0] if exc.args else None)
                        break
                    except Exception, exc:                                            
                        yielded.genfunc.close()
                        yielded2 = gen.throw(exc)
                        new_tosend = (yield yielded2)
                        break                        
                    nested_tosend = (yield nested_yielded)
            else:
                new_tosend = (yield yielded)
            tosend = new_tosend
    @wraps(genfunc)
    def _wrapper(*args, **kwargs):
        return _process(genfunc(*args, **kwargs))
    return _wrapper
