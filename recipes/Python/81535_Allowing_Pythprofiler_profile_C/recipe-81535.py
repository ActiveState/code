"""profilewrap.py:
Wraps C functions, objects and modules in dynamically-generated Python code
so you can profile them.  Here's an example using the rotor encryption module:

>>> import profilewrap, rotor, profile
>>> r = profilewrap.wrap( rotor.newrotor( 'key' ) )
>>> profile.run( "r.encrypt( 'Plaintext' )" )

This will produce output including something like this:

    1    0.003    0.003    0.003    0.003 PW_rotor.py:1(encrypt)

See the function _profileMe for examples of wrapping C functions, objects and
modules.  Run profilewrap.py to see the output from profiling _profileMe."""

import new, types

def _functionProxy( f, *args, **kwargs ):
   """The prototype for the dynamic Python code wrapping each C function."""
   return apply( f, args, kwargs )

class _ProfileWrapFunction:
   """A callable object that wraps each C function we want to profile."""
   def __init__( self, wrappedFunction, parentName="unnamed" ):
      # Build the code for a new wrapper function, based on _functionProxy.
      filename = "PW_%s.py" % parentName
      name = wrappedFunction.__name__
      c = _functionProxy.func_code
      newcode = new.code( c.co_argcount, c.co_nlocals, c.co_stacksize,
                          c.co_flags, c.co_code, c.co_consts, c.co_names,
                          c.co_varnames, filename, name, 1, c.co_lnotab )
      
      # Create a proxy function using the new code.
      self._wrapper = new.function( newcode, globals() )
      self._wrappedFunction = wrappedFunction
      
   def __call__( self, *args, **kwargs ):
      return apply( self._wrapper, (self._wrappedFunction,) + args, kwargs )


class _ProfileWrapObject:
   """A class that wraps an object or a module, and dynamically creates a
      _ProfileWrapFunction for each method.  Wrappers are cached for speed."""
   def __init__( self, wrappedObject ):
      self._wrappedObject = wrappedObject
      self._cache = {}
      
   def __getattr__( self, attrName ):
      # Look for a cached reference to the attribute and if it isn't there,
      # fetch it from the wrapped object.
      notThere = 'Not there'
      returnAttr = self._cache.get( attrName, notThere )
      if returnAttr is notThere:
         attr = getattr( self._wrappedObject, attrName, notThere )
         if attr is notThere:
            # The attribute is missing - let it raise an AttributeError.
            getattr( self._wrappedObject, attrName )
         
         # We only wrap C functions, which have the type BuiltinMethodType.
         elif isinstance( attr, types.BuiltinMethodType ):
            # Base the fictitious filename on the module name or class name.
            if isinstance( self._wrappedObject, types.ModuleType ):
               objectName = self._wrappedObject.__name__
            else:
               objectName = type( self._wrappedObject ).__name__
            returnAttr = _ProfileWrapFunction( attr, objectName )
            self._cache[ attrName ] = returnAttr
         
         # All non-C-function attributes get returned directly.
         else:
            returnAttr = attr
         
      return returnAttr


def wrap( wrappee ):
   """Wrap the given object, module or function in a Python wrapper."""
   if isinstance( wrappee, types.BuiltinFunctionType ):
      return _ProfileWrapFunction( wrappee )
   else:
      return _ProfileWrapObject( wrappee )

def _profileMe():
   # Wrap a built-in C function.
   wrappedEval = wrap( eval )
   print wrappedEval( '1+2*3' )
   
   # Replace a C module with its wrapped equivalent.
   import os
   os = wrap( os )
   print os.getcwd()

   # Wrap a C object.
   import rotor
   r = wrap( rotor.newrotor( 'key' ) )
   print repr( r.encrypt( 'Plaintext' ) )
   
if __name__ == '__main__':
   import profile
   profile.run( '_profileMe()' )
