import collections
from functools import partial
from pysistence.func import trampoline

def setup():
    print 'Setting up...'
    return True
def first_step():
    print 'First step...'
    return True
def second_step():
    print 'Second step...'
    return True
def wait():
    print 'Waiting...'
    return True
def stop():
    print 'Stopping...'
    return True

State = collections.namedtuple('State', 'name function on_success on_failure')

do_start = State(name='start', function=setup, on_success='do_first_step', on_failure='do_stop')
do_first_step = State(name='first_step', function=first_step, on_success='do_second_step', on_failure='do_stop')
do_second_step = State(name='second_step', function=second_step, on_success='do_wait', on_failure='do_stop')
do_wait = State(name='wait', function=wait, on_success='do_first_step', on_failure='do_stop')
do_stop = State(name='stop', function=stop, on_success=None, on_failure=None)

def state_machine(state):
    if state.function():
        new_state = globals().get(state.on_success, None)
    else:
        new_state = globals().get(state.on_failure, None)
    if new_state:
        return partial(state_machine, new_state)

if __name__ == '__main__':        
    trampoline(state_machine, do_start)
