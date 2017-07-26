def norec(an=0,defret=None,initial=[]):
    """ Recursion/loop prevention function decorator

        For example, could be used when traversing a graph, which nodes assigned
        unique IDs and you would like to avoid loops.

        Keyword arguments:
        an -- position of function argument, which is used as unique id (0-based)
        defret -- default return value, which is returned when recursion is detected
        initial -- initial content of call stack. Array of unique ids

        Vadim Zaliva <lord@crocodile.org>
    """
    class decorate:
        def __init__(self):
            self.cs=initial
            
        def __call__(self, f):
            def new_f(*args, **kwds):
                id=args[an]
                if id in self.cs:
                    #print "recursion detected at '%s' in %s" % (id, str(self.cs))
                    return defret
                else:
                    self.cs.append(id)
                    x = f(*args, **kwds)
                    self.cs.remove(id)
                    return x
            return new_f
    return decorate()
