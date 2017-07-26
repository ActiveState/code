#! /usr/bin/env python

""" Generic finite state machine class
    Initialise the class with a list of tuples - or by adding transitions
"""

class fss(object):
    def __init__(self, states=[]):
        self._states=states
        self.currentState = None

    def start(self,startState=None):
        """ Start the finite state machine
        """
        if not startState or not (startState in [x[0] for x in self._states]):
            raise ValueError("Not a valid start state")
        self.currentState = startState

    def stop(self):
        """ Stop the finite state machine
        """
        self.startState = None
    
    def addTransition(self,fromState, toState, testFunc):
        """ Add a state transition to the list, order is irellevant, loops are undetected 
            Can only add a transition if the state machine isn't started.
        """
        if not self.currentState:
            raise ValueError("StateMachine already Started - cannot add new transitions")

        # add a transition to the state table
        self._states.append( (fromState, toState,testFunc))

    def event(self, value):
        """ Trigger a transition - return a tuple (<new_state>, <changed>)
            Raise an exception if no valid transition exists.
            Callee needs to determine if the value should be consumed or re-used
        """
        if not self.currentState:
            raise ValueError("StateMachine not Started - cannot process event")

        # get a unique list of next states which are valid       
        self.nextState = list(set( \
                    [ x[1] for x in self._states\
                    if x[0] == self.currentState \
                            and (x[2]==True or (callable(x[2]) and x[2](value))) ] ) ) 

        if not self.nextState: 
            raise ValueError("No Transition defined from state {0} with value '{1}'".format(self.currentState, value))
        elif len(self.nextState) > 1:
            raise ValueError("Ambiguous transitions from state {0} with value '{1}' ->  New states defined {2}".format(self.currentState, value, self.nextState))
        else:
            self.currentState, ret = (self.nextState[0], True) \
                    if self.currentState != self.nextState[0] else (self.nextState[0], False)
            return self.currentState, ret

    def CurrentState(self):
        """ Return the current State of the finite State machine
        """
        return self.currentState

# Example code - showing populates of the state machine in the constructor
# the Machine could also be constructed by multiple calls to addTransition method
# Example code is a simple tokeniser 
# Machine transitions back to the Start state whenever the end of a token is detected

if __name__ == "__main__":
    fs = fss( [ ("Start","Start",lambda x: x.isspace() ),
                ("Start","Identifier",str.isalpha),
                ("Identifier","Identifier", str.isalnum),
                ("Identifier","Start",lambda x: not x.isalnum() ),
                ("Start","Operator", lambda x: x in "=+*/-()"),
                ("Operator","Start", True),
                ("Start","Number",str.isdigit),
                ("Number","Number",lambda x: x.isdigit() or x == "." ),
                ("Number","Start",lambda x: not x.isdigit() and x != "." ),
                ("Start","StartQuote",lambda x: x == "\'"),
                ("StartQuote","String", lambda x: x != "\'"),
                ("String","String",lambda x: x != "\'"),
                ("String","EndQuote", lambda x: x == "\'"),
                ("EndQuote","Start", True ) ] )

    fs.start("Start")

    a = "    x123=MyString+123.65-'hello'*value"
    c = 0 
    while c < len(a):
        ret = fs.event(a[c])
        print "{0}-> {1}".format(a[c], ret)
        # Make sure a transition back to start (from something else) does not consume the character.
        if ret[0] != "Start" or (ret[0] == "Start" and ret[1] == False):
            c += 1
