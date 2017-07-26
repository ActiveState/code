###
#
#  W A R N I N G 
#  
#  This recipe is obsolete! 
#  
#  When you are looking for copying and pickling functionality for generators
#  implemented in pure Python download the 
#
#             generator_tools 
#
#  package at the cheeseshop or at www.fiber-space.de
#              
###


import new
import copy
import types
import sys
from opcode import*


def copy_generator(f_gen):
    '''
    Function used to copy a generator object.

    @param f_gen: generator object.
    @return: pair (g_gen, g) where g_gen is a new generator object and g a generator
             function g producing g_gen. The function g is created from f_gen.gi_frame.

    Usage: function copies a running generator.

        def inc(start, step = 1):
            i = start
            while True:
                yield i
                i+= step

        >>> inc_gen = inc(3)
        >>> inc_gen.next()
        3
        >>> inc_gen.next()
        4
        >>> inc_gen_c, inc_c = copy_generator(inc_gen)
        >>> inc_gen_c.next() == inc_gen.next()
        True
        >>> inc_gen_c.next()
        6

    Implementation strategy:

        Inspecting the frame of a running generator object f provides following important
        information about the state of the generator:

           - the values of bound locals inside the generator object
           - the last bytecode being executed

        This state information of f is restored in a new function generator g in the following way:

           - the signature of g is defined by the locals of f ( co_varnames of f ). So we can pass the
             locals to g inspected from the current frame of running f. Yet unbound locals are assigned
             to None.

             All locals will be deepcopied. If one of the locals is a generator object it will be copied
             using copy_generator. If a local is not copyable it will be assigned directly. Shared state
             is therefore possible.

           - bytecode hack. A JUMP_ABSOLUTE bytecode instruction is prepended to the bytecode of f with
             an offset pointing to the next unevaluated bytecode instruction of f.

    Corner cases:

        - an unstarted generator ( last instruction = -1 ) will be just cloned.

        - if a generator has been already closed ( gi_frame = None ) a ValueError exception
          is raised.

    '''
    if not f_gen.gi_frame:
        raise ValueError("Can't copy closed generator")
    f_code = f_gen.gi_frame.f_code
    offset = f_gen.gi_frame.f_lasti
    locals = f_gen.gi_frame.f_locals

    if offset == -1:  # clone the generator
        argcount = f_code.co_argcount
    else:
        # bytecode hack - insert jump to current offset 
        # the offset depends on the version of the Python interpreter
        if sys.version_info[:2] == (2,4):
            offset +=4
        elif sys.version_info[:2] == (2,5):
            offset +=5
        start_sequence = (opmap["JUMP_ABSOLUTE"],)+divmod(offset, 256)[::-1]
        modified_code = "".join([chr(op) for op in start_sequence])+f_code.co_code
        argcount = f_code.co_nlocals

    varnames = list(f_code.co_varnames)
    for i, name in enumerate(varnames):
        loc = locals.get(name)
        if isinstance(loc, types.GeneratorType):
            varnames[i] = copy_generator(loc)[0]
        else:
            try:
                varnames[i] = copy.deepcopy(loc)
            except TypeError:
                varnames[i] = loc

    new_code = new.code(argcount,
             f_code.co_nlocals,
             f_code.co_stacksize,
             f_code.co_flags,
             modified_code,
             f_code.co_consts,
             f_code.co_names,
             f_code.co_varnames,
             f_code.co_filename,
             f_code.co_name,
             f_code.co_firstlineno,
             f_code.co_lnotab)
    g = new.function(new_code, globals(),)
    g_gen = g(*varnames)
    return g_gen, g
