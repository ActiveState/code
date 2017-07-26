""" Create portable serialized representations of Python <code> Objects"""

import new
import pickle


def co_dumps(s):
    """pickles a code object,arg s is the string with code
    returns the code object pickled as a string"""
    co = compile(s,'<string>','exec')
    co_tup=[co.co_argcount,co.co_nlocals, co.co_stacksize,co.co_flags,
    co.co_code,co.co_consts,co.co_names,co.co_varnames,co.co_filename,
    co.co_name,co.co_firstlineno,co.co_lnotab]
    return pickle.dumps(co_tup)

def co_dumpf(s,f):
    """similar to co_dumps() but instead of returning the string, writes
    the pickled object to an opened file(f) to be retrieved with co_loadf()"""
    
    co = compile(s,'<string>','exec')
    co_tup=[co.co_argcount,co.co_nlocals, co.co_stacksize,co.co_flags,
    co.co_code,co.co_consts,co.co_names,co.co_varnames,co.co_filename,
    co.co_name,co.co_firstlineno,co.co_lnotab]
    pickle.dump(co_tup,f)
    
def co_loads(s):
    """loads a code object pickled with co_dumps()
    return a code object ready for exec()"""
    r = pickle.loads(s)
    return new.code(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11])

def co_loadf(f):
    """loads a code object from a file"""
    r = pickle.load(f)
    return new.code(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11])


def test():
    string_with_code = 'print "hello co_pickle"'
    pickled_code_object = co_dumps(string_with_code)
    #print code_object
    recovered_code_object = co_loads(pickled_code_object)
    exec(recovered_code_object)
    
