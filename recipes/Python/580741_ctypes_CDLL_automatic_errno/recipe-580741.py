import ctypes

class CDLL_errno(ctypes.CDLL):

    class _FuncPtr(ctypes._CFuncPtr):
        _flags_ = ctypes._FUNCFLAG_CDECL | ctypes._FUNCFLAG_USE_ERRNO
        _restype_ = ctypes.c_int

        def __call__(self, *args):
            ctypes.set_errno(0)
            try:
                return ctypes._CFuncPtr.__call__(self, *args)
            finally:
                errno = ctypes.get_errno()
                if errno:
                    import os
                    raise IOError(errno, os.strerror(errno))

    def __init__(self, *args, **kw):
        ctypes.CDLL.__init__(self, *args, **kw)
        del self._FuncPtr
