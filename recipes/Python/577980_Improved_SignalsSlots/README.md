## Improved Signals/Slots implementation in PythonOriginally published: 2011-12-12 22:47:25 
Last updated: 2011-12-12 22:47:25 
Author: Christopher S. Case 
 
I've modified the excellent [recipe 576477](http://code.activestate.com/recipes/576477-yet-another-signalslot-implementation-in-python/) to allow for non method functions as well as method functions. This implementation also uses a WeakKeyDictionary instead of a WeakValueDictionary for reasons of code simplification/style.