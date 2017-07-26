import pdb

IO = lambda s: (s.stdin, s.stdout)

def rpdb(F):
    """
    robot python debugger -- usage:
    @rpdb
    def keyword_method(self, arg1, arg2, ...):
        # stuff here ...
        rpdb.set_trace() # set breakpoint as usual
        # more code ...
    """
    setattr(rpdb, 'set_trace', pdb.set_trace)
    builtinIO = IO(sys)
    def _inner(*args, **kwargs):
        robotIO = IO(sys) # robot has hijacked stdin/stdout
        pdb.sys.stdin, pdb.sys.stdout = builtinIO
        retval = F(*args, **kwargs)
        sys.stdin, sys.stdout = robotIO
        return retval
    return _inner
