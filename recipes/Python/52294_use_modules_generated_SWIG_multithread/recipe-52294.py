// Typemap for SWIG by Mark Hammond, as posted on comp.lang.python
//
//
// Map API functions that return BOOL to
// functions that return None, but raise exceptions.
// These functions must set the win32 LastError.

// These functions automatically release the thread lock for the
// duration of the function
// 
%typedef BOOL BOOLAPI

%typemap(python,except) BOOLAPI {
	Py_BEGIN_ALLOW_THREADS
	$function
        Py_END_ALLOW_THREADS
        if (!$source)  {
              $cleanup
               return PyWin_SetAPIError("$name");
        }
}


                
