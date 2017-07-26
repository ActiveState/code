'''a very simple idiom for a state machine'''

from random import random
from time import sleep


# Each of the state functions below performs some action and then implements
# logic to choose next state.  Each state function returns the next state.

def state0():
    print "state0"
    # delay and decision path to simulate some application logic
    sleep(.5)
    if random()>.5:
        return state1
    else:
        return state2

def state1():
    print "state1"
    # delay and decision path to simulate some application logic
    sleep(.5)
    if random()>.5:
        return state0
    else:
        return state2

def state2():
    print "state2"
    # delay and decision path to simulate some application logic
    sleep(.5)
    if random()>.5:
        return state0
    else:
        return None

state=state0    # initial state
while state: state=state()  # launch state machine
print "Done with states"
