# CLASS NAME: DLLInterface
#
# Author: Larry Bates
#
# Written: 08/14/2002
#
# Description: This is a base class for implementing a class interface
# to call general DLL libraries.  You should build your class using
# this class as the base class.  Define methods for each function of
# the DLL that you wish to implement.
#
import os, sys
import calldll
from dynwin.windll import cstring, membuf

class DLLInterface:
    '''
    class DLLInterface is used as a base class as a general interface class to
    Microsoft Windows DLLs.  None  of the methods of this class should be
    called directly.  Subclass this class and have subclass' methods
    make calls to _dllcall to call functions from the DLL.
    '''

    #--------------------------------------------------------------------------------------------
    # Example usage:
    #
    # class anydll(DLLInterface):
    #    def function1 (self, arg1, arg2, ..., argn)
    #        #
    #        # code goes here to implement function1 from the DLL
    #        # as a method of anydll class.
    #        #
    #        # Syntax of _dllcall function is (function in .DLL,
    #        #                                 argument types,    ['llh' is long, long, short]
    #        #                                 return code type,  ['h' is short]
    #        #                                 arguments in a tuple)              
    #        #
    #        result=self._dllcall('function1',
    #                             'lll',
    #                             'h',
    #                             (arg1,
    #                              arg2,
    #                              arg3,
    #                               .
    #                               .
    #                               .
    #                              argn))
    #        return result
    #
    # this would then be executed using:
    #
    # D=anydll(DLLPath)
    # result=d.function(arg1, arg2, ..., argn)
    #
    # argument types = 'h'-short, 'l'-long, 's'-string (null terminated using helper function
    #                                                   cstring in dynwin)
    #--------------------------------------------------------------------------------------------
       
    def __init__(self, DLLPath, ext='.dll'):
        self._debug=0
        self._trace=0
        self._loaded=0
        self._funcs={}
        self._DLLName=os.path.split(DLLPath)[1]+ext  # Save DLL filename
        if self._trace: print "creating _handle"
        #
        # Load the DLL library (if not already loaded) and save a
        # handle to it in self._handle
        #
        if not self._loaded:
            self._handle=calldll.load_library(DLLPath+ext)
            #
            # If I didn't get a handle, DLL wasn't loaded
            #
            if not self._handle:
                raise SystemError, "couldn't load module '%s'" % self._DLLName
            else:
                self._loaded=1
            
        if self._trace: print "handle=",self._handle

        if self._trace: print "Leaving __init__"
        return

    def unload(self):
        if self._loaded and self._handle:
            calldll.free_library(self._handle)
            
        self._loaded=0
        self._handle=0
        self._funcs={}
        return

    def _dlladdr(self, func_name):
        #
        # This method uses the function name (func_name) and looks into the .DLL
        # to find the address that should be used to call that function.
        #
        if self._trace: print "self._handle=",self._handle
        if self._trace: print "_dlladdr to get address of %s func" % func_name
        if not self._handle:
            raise SystemError, "No handle found for %s" % self._DLLName
        #
        # See if I've called this func_name before.  If I have, I have saved
        # the address in self._funcs dictionary object so I don't have to call
        # calldll.get_proc_address repeatedly.  A method of "caching" the addresses.
        # to hopefully speed things up a little.
        #
        try:
            addr=self._funcs[func_name]
        except:
            addr=calldll.get_proc_address(self._handle, func_name)
            self._funcs[func_name]=addr
            
        if self._trace:
            print "leaving _dlladdr, function %s has calling address=%i" % (func_name, addr)
            print ""
        #
        # Return the address of this function so it can be called by calldll
        #
        if addr: return addr
        else:    raise SystemError, "%s has no function named '%s'" % (self._DLLName, func_name)

    def _dllcall(self, function_name,arg_format_string, result_format_string, args):
        #
        # This method is used to make the call to the DLL function
        # Arguments are:
        #
        # function_name - String containing the name of the function to call
        # arg_format_string - this is a string that contains the format of the
        #                     arguments that are to be passed to the function.
        #                     These can be one of:
        #                     l - long integer (or address)
        #                     h - short integer (half)
        #                     s - string
        #
        #                     Example: "lllh"
        #
        # result_format_string - The result will be either l or h, returned by
        #                        function
        # args - This is a tuple (even if there is only one argument)
        #
        #                     Example: (x,) or (a,b,c,d)
        #
        if self._trace: print "Entering _dllcall to call function=",function_name
        result=calldll.call_foreign_function(self._dlladdr(function_name),
                                                           arg_format_string,
                                                           result_format_string,
                                                           args)
        #
        # If result_format_string is "h" mask out high bits of result
        #
        if result_format_string in ('h','H'):
            result=result & 0xffff
            
        #
        # If result_format_string is "s", strip off trailing null character
        #
        if result_format_string in ('s','S'):
            result=result[:-1]

        return result          
