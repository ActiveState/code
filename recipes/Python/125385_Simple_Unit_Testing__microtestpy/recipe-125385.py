# mircotest.py

import sys
import traceback
class TestException(Exception): pass

def test(modulename, verbose=None, log=sys.stdout):
    '''Execute all functions in named module with __test__ in the name
    that take no arguments
    modulename -- name of the module to be tested.
    verbose    -- If true print sequence of test names as they are executed
    Returns None on success, raises exception on failure.'''

    module = __import__(modulename)
    total_tested = 0
    total_failed = 0
    for name in dir(module):
        if name.find('__test__') >= 0:
            if type(module.__dict__[name]) == type(unittest):
                if (module.__dict__[name].func_code.co_argcount) == 0:
                    if verbose:
                        print >> log, 'Testing %s' % name
                    try:
                        total_tested += 1
                        module.__dict__[name]()
                    except Exception, e:
                        total_failed += 1
                        print >> sys.stderr, '%s.%s FAILED' % (modulename, name)
                        traceback.print_exc()
    message = 'Module %s failed %s out of %s unittests.' %\
              (modulename, total_failed, total_tested)
    if total_failed > 0:
        raise TestException(message)
    if verbose:
        print >> log, message
        
def __test__():
    print 'in __test__'

import pretest
pretest.pretest('microtest', 1)
