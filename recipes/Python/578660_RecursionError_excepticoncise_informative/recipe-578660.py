'''
@since: 15/09/2013
@version: 0.3 06/07/2015

@author: Elazar Gershuni (elazarg at gmail)
'''

import sys
import traceback


def _find_last_cycle(tb):
    call_names = set()
    size = 0
    for i, call in enumerate(reversed(tb)):
        #call is not hashable in python3.5, but it has a name
        name = getattr(call, 'name', None) or hash(call)
        if size == 0:
            call_names.add(name)
            if call == tb[-1]:
                size = i
        elif name not in call_names:
            length = i
            break
    return size, length


def is_recursion_error(exctype, trace):
    if exctype.__name__ == 'RecursionError':
        return True
    if exctype is not RuntimeError:
        return False
    # prior to python3.5 there's no RecursionError,
    # so we check the size
    tb = traceback.extract_tb(trace)
    return len(tb) == sys.getrecursionlimit()


def cycle_detect_excepthook(exctype, value, trace):
    if is_recursion_error(exctype, trace):
        tb = traceback.extract_tb(trace)
        size, length = _find_last_cycle(tb)
        count = round(length / size, 2)
        if count >= 2:
            traceback.print_exception(exctype, value, trace, len(tb) - length + size)
            # sadly, we have no standard way to add this line to the real error stream
            sys.stderr.write('{} occurrences of cycle of size {} detected\n'
                            .format(count, size))
            return
    sys.__excepthook__(exctype, value, trace)

# the excepthook 
sys.excepthook = cycle_detect_excepthook

if __name__ == '__main__':
    def p2(): p0()
    
    def p1(): p2()
    
    def p0(): p1()
    
    def bar():
        p0()
        
    bar()


    '''
    Output in interactive mode:
    
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 2, in bar
      File "<stdin>", line 1, in p0
      File "<stdin>", line 1, in p1
      File "<stdin>", line 1, in p2
    RuntimeError: maximum recursion depth exceeded
    332.67 occurrences of cycle of size 3 detected    
    '''
