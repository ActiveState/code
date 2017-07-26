__all__=[]
_rgb_files = [open('/tmp/rgb_debug.txt','w')]
import sys, time
_rgb_auto_flush=1
def rgb_time(offs=1):
    t = time.time()
    if offs: return t-_rgb_t0
    return t
_rgb_t0=rgb_time(0)
def rgb_debug(*msg,**kwds):
    msg = ' '.join(map(str,msg)) + '\n'
    for f in _rgb_files:
        f.write(msg)
        if _rgb_auto_flush:
            flush = getattr(f,'flush',None)
            if flush: flush()
def rgb_pprint(*obj):
    if obj:
        if isinstance(obj[0],(str,unicode)):
            rgb_debug(obj[0])
            obj = obj[1:]
        import pprint
        for o in obj:
            for f in _rgb_files:
                pprint.pprint(o,f)

def rgb_stack(*msg,**kwds):
    import inspect
    rgb_debug(*msg)
    i = 1
    while 1:
        f = sys._getframe(i)
        if f.f_globals.get('_rgb_t0',None) is not _rgb_t0: break
        i += 1
    F = inspect.stack()
    frameCount = kwds.get('_frameCount',0) 
    showLocals = kwds.get('_showLocals',0) 
    if not frameCount:
        F = F[i:]
    else:
        F = F[i:i+frameCount]
    for f in F:
        rgb_debug('file:',f[1],'line:',f[2],'in',f[3])
        for l in f[4]: rgb_debug(l)
        if showLocals:
            rgb_debug('    locals=%r' % f[0].f_locals)

class _RGB_Wrapper(object):
    def __init__(self,func,funcname=None,show=0,show_kwds={}):
        self.func = func
        self.funcname = funcname or func.__name__
        if not callable(show):
            show=show and rgb_stack or rgb_debug
        self.show = show
        self.show_kwds= show_kwds
        self.called = 0
    def __call__(self,*args,**kwds):
        func = self.func
        if not self.called:
            self.called = 1
            try:
                self.show('%s(*%r,**%r) called' % (self.funcname,args,kwds),**self.show_kwds)
            finally:
                self.called = 0
        return func(*args,**kwds)

def rgb_wrap(func,show=1,funcname=None,show_kwds={}):
    return _RGB_Wrapper(func,funcname,show,show_kwds=show_kwds)

class rgb_watch_writes:
    def __init__(self,f,cb,*cbargs):
        self._f = f
        self._cb = cb
        self._cbargs = cbargs
    def write(self,msg):
        self._cb(*((msg,)+self._cbargs))
        self._f.write(msg)
    def __getattr__(self,a):
        return getattr(self._f,a)

def rgb_print_exc(*msg):
    if msg: rgb_debug(*msg)
    import traceback
    for f in _rgb_files: traceback.print_exc(file=f)
    if _rgb_auto_flush: rgb_flush()

def rgb_add_file(f):
    if f not in _rgb_files: _rgb_files.append(f)

def rgb_auto_flush(v=1):
    _rgb_auto_flush=v

def rgb_flush():
    for f in _rgb_files:
        flush = getattr(f,'flush',None)
        if flush: flush()
    
import __builtin__
__builtin__.rgb_debug = rgb_debug
__builtin__.rgb_stack = rgb_stack
__builtin__.rgb_pprint = rgb_pprint
__builtin__.rgb_time = rgb_time
__builtin__.rgb_print_exc = rgb_print_exc
__builtin__.rgb_auto_flush = rgb_auto_flush
__builtin__.rgb_flush = rgb_flush
__builtin__.rgb_wrap = rgb_wrap
__builtin__.rgb_add_file = rgb_add_file
__builtin__.rgb_watch_writes = rgb_watch_writes
rgb_debug.__module__=sys.modules['rgb_debug']
sys.modules['rgb_debug'] = rgb_debug
