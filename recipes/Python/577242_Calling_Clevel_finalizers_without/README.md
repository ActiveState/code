## Calling (C-level) finalizers without __del__  
Originally published: 2010-05-23 22:02:06  
Last updated: 2011-07-02 18:42:08  
Author: Benjamin Peterson  
  
This recipe is meant for Python classes wrapping ctypes bindings where a C-level finalizer must be invoked when the wrapper is destroyed. It uses weakref callbacks to avoid problems with ``__del__``.