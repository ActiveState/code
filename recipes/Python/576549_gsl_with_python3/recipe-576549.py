'''
    module gls_setup, file gsl_setup.py

    load the gsl shared libraries and ctypes

        consider gsl_set_error_handler_off();
        (gsl errors cause core dumps which I choose to live with for now)
'''
import sys
if sys.version_info[0] != 3:
    raise Exception('This code has been tried in python version 3')

from ctypes import *
from array import array

# probably add some OS specific code here to encompass more than linux
# load dependencies first, making the symbols available.
gslcblas = CDLL('libgslcblas.so',mode=RTLD_GLOBAL)
gsl = CDLL('libgsl.so')

def setup(f,argument_types_list,result_type=c_long):
    f.argtypes = argument_types_list
    f.restype = result_type
    return f

def as_array(a,typecode='d'):
    return (
        a if (isinstance(a,array) and a.typecode == typecode)
        else array(typecode,a)
    )

def ADDRESS(a):
    return a.buffer_info()[0]
