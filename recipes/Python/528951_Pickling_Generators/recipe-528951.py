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

import pickle
import types

class any_obj:
    "Used to create objects for spawning arbitrary attributes by assignment"

class GeneratorSnapshot(object):
    '''
    Object used to hold data for living generators. 
    '''
    def __init__(self, f_gen):
        f_code = f_gen.gi_frame.f_code
        self.gi_frame = any_obj()
        self.gi_frame.f_code   = any_obj()
        self.gi_frame.f_code.__dict__.update((key, getattr(f_code, key))
                                                   for key in dir(f_code) if key.startswith("co_"))
        self.gi_frame.f_lasti  = f_gen.gi_frame.f_lasti
        self.gi_frame.f_locals = {}
        for key, value in f_gen.gi_frame.f_locals.items():
            if isinstance(value, types.GeneratorType):
                self.gi_frame.f_locals[key] = GeneratorSnapshot(value)
            else:
                self.gi_frame.f_locals[key] = value

def pickle_generator(f_gen, filename):
    '''
    @param f_gen: generator object
    @param filename: destination file for pickling generator
    '''
    output_pkl = open(filename, "wb")
    pickle.dump(GeneratorSnapshot(f_gen), output_pkl)

def unpickle_generator(filename):
    '''
    @param filename: source file of pickled generator
    '''
    input_pkl = open(filename, "rb")
    gen_snapshot = pickle.load(input_pkl)
    return copy_generator(gen_snapshot)[0]                
