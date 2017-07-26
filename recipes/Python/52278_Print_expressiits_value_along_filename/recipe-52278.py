from sys import exc_info, stderr
import types, string
from traceback import *

def _caller_symbols():
    try:
        raise StandardError
    except StandardError:
        t = exc_info()[2].tb_frame
        return (t.f_back.f_back.f_globals,t.f_back.f_back.f_locals)


def printexpr(expr_string):
    """ printexpr(expr) - 
        print the value of the expression, along with linenumber and filename.
    """

    stack = extract_stack ( )[-2:][0]
    actualCall = stack[3]
    left = string.find ( actualCall, '(' )
    right = string.rfind ( actualCall, ')' )
    caller_globals,caller_locals = _caller_symbols()
    expr = eval(expr_string,caller_globals,caller_locals)
    varType = type( expr )
    stderr.write("%s:%d>  %s == %s  (%s)\n" % (
        stack[0], stack[1],
        string.strip( actualCall[left+1:right] )[1:-1],
        repr(expr), str(varType)[7:-2]))
