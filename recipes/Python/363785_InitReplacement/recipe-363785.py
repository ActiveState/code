"""HACK: Make module.ClassWithUnsafeInit safe."""

import module


def enable_safety():
    """HACK: Make ClassWithUnsafeInit safe.

    module.ClassWithUnsafeInit does something unsafe.  

    Move the old ClassWithUnsafeInit.__init__ method out of the way--name it
    _NowSafeOrigInit.  Move the old ClassWithUnsafeInit class out of the
    way--name it _NowSafeClassWithUnsafeInit.  Create a new function,
    _NowSafeNewClassWithUnsafeInit, in place of the ClassWithUnsafeInit class
    that instantiates _NowSafeClassWithUnsafeInit and then calls
    _NowSafeClassWithUnsafeInit._NowSafeOrigInit (thanks go to Paul Abrams for
    this second part of the hack).  Last of all, ClassWithUnsafeInit has a
    ClassWithUnsafeInitClass attribute.  Set this to
    _NowSafeNewClassWithUnsafeInit.  I accept the fact that there's probably a
    special place in programmer hell for me (and Paul).

    This must be called exactly once, and it must be called before
    ClassWithUnsafeInit is used for the first time.

    """
    ClassWithUnsafeInit._NowSafeOrigInit = ClassWithUnsafeInit.__init__
    module._NowSafeClassWithUnsafeInit = ClassWithUnsafeInit
    ClassWithUnsafeInit = _NowSafeNewClassWithUnsafeInit
    ClassWithUnsafeInitClass = _NowSafeNewClassWithUnsafeInit


def _NowSafeNewClassWithUnsafeInit(*args, **kargs):
    fs = module._NowSafeClassWithUnsafeInit()
    # Do whatever you need here.
    fs._NowSafeOrigInit(*args, **kargs) 
    return fs
