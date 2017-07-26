# pretest.py
"""
Usage: To execute your tests each time your module is compiled, add this line
at the end of your module.  Be sure to edit pretest to call your favorite test 
runner in place of microtest.test.

pretest.pretest('mymodule')
"""
import os
import microtest
import sys

def pretest(modulename, verbose=None, force=None, deleteOnFail=0, 
            log=sys.stdout):
    # import module
    module = __import__(modulename)

    # only test uncompiled modules unless forced
    if module.__file__[-3:] == '.py' or force:

        # kick off your tests with your favorite test suite
        if microtest.test(modulename, verbose, log):
            pass # all tests passed
        elif deleteOnFail:
            
            # Cream the pyc file so we run the test suite next time 'round
            filename = module.__file__
            if filename[-3:] == '.py':
                filename = filename + 'c'
            try:
                os.remove(filename)
            except OSError:
                pass
        
