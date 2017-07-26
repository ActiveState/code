#! /usr/bin/env python

""" Generic finite state machine class
    Initialise the class with a list of tuples - or by adding transitions
    Tony Flury - November 2012
    Released under an MIT License - free to use so long as the author and other contributers are credited.
"""

class fsm(object):
    """ A simple to use finite state machine class.
        Allows definition of multiple states, condition functions from state to state and optional callbacks
    """
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
        # Bug fix 15 Dec 2012 - self.currentState should be reset, not startState - Identified by Holger Waldmann
        self.currentState = None
    
    def addTransition(self,fromState, toState, condition, callback=None):
        """ Add a state transition to the list, order is irellevant, loops are undetected 
            Can only add a transition if the state machine isn't started.
        """
        if not self.currentState:
            raise ValueError("StateMachine already Started - cannot add new transitions")

        # add a transition to the state table
        self._states.append( (fromState, toState,condition, callback))

    def event(self, value):
        """ Trigger a transition - return a tuple (<new_state>, <changed>)
            Raise an exception if no valid transition exists.
            Callee needs to determine if the value will be consumed or re-used
        """
        if not self.currentState:
            raise ValueError("StateMachine not Started - cannot process event")

        # get a list of transitions which are valid       
        self.nextStates = [ x for x in self._states\
                            if x[0] == self.currentState \
                            and (x[2]==True or (callable(x[2]) and x[2](value))) ] 

        if not self.nextStates: 
            raise ValueError("No Transition defined from state {0} with value '{1}'".format(self.currentState, value))
        elif len(self.nextStates) > 1:
            raise ValueError("Ambiguous transitions from state {0} with value '{1}' ->  New states defined {2}".format(self.currentState, value, [x[0] for x in self.nextStates]))
        else:
            if len(self.nextStates[0]) == 4:
                current, next, condition, callback = self.nextStates[0]
            else:
                current, next, condition = self.nextStates[0]
                callback = None

            self.currentState, changed = (next,True) \
                    if self.currentState != next else (next, False)
            
            # Execute the callback if defined
            if callable(callback):
                callback(self, value)

            return self.currentState, changed

    def CurrentState(self):
        """ Return the current State of the finite State machine
        """
        return self.currentState


# -------------------------------------------------------------------------------------------------
# Example classes to demonstrate the use of the Finite State Machine Class
# They implement a simple lexical tokeniser.
# These classes are not neccesary for the FSM class to work.
# -------------------------------------------------------------------------------------------------

# Simple storage object for each token
class token(object):
    def __init__(self, type):
        self.tokenType = type
        self.tokenText = ""
    
    def addCharacter(self, char):
        self.tokenText += char

    def __repr__(self):
        return "{0}<{1}>".format(self.tokenType, self.tokenText)


# Token list object - demonstrating the definition of state machine callbacks
class tokenList(object):
    def __init__(self):
        self.tokenList = []
        self.currentToken = None
        
    def StartToken(self, fss, value):
        self.currentToken = token(fss.CurrentState())
        self.currentToken.addCharacter(value)

    def addCharacter(self, fss, value):
        self.currentToken.addCharacter(value)

    def EndToken(self, fss, value):
        self.tokenList.append(self.currentToken)
        self.currentToken = None


# Example code - showing population of the state machine in the constructor
# the Machine could also be constructed by multiple calls to addTransition method
# Example code is a simple tokeniser 
# Machine transitions back to the Start state whenever the end of a token is detected
if __name__ == "__main__":
    t = tokenList()

    fs = fsm( [ ("Start","Start",lambda x: x.isspace() ),
                ("Start","Identifier",str.isalpha, t.StartToken ),
                ("Identifier","Identifier", str.isalnum, t.addCharacter ),
                ("Identifier","Start",lambda x: not x.isalnum(), t.EndToken ),
                ("Start","Operator", lambda x: x in "=+*/-()", t.StartToken ),
                ("Operator","Start", True, t.EndToken),
                ("Start","Number",str.isdigit, t.StartToken ),
                ("Number","Number",lambda x: x.isdigit() or x == ".", t.addCharacter ),
                ("Number","Start",lambda x: not x.isdigit() and x != ".", t.EndToken ),
                ("Start","StartQuote",lambda x: x == "\'"),
                ("StartQuote","String", lambda x: x != "\'", t.StartToken),
                ("String","String",lambda x: x != "\'", t.addCharacter ),
                ("String","EndQuote", lambda x: x == "\'", t.EndToken ),
                ("EndQuote","Start", True ) ] )

    fs.start("Start")

    a = "    x123=MyString+123.65-'hello'*value"
    c = 0 
    while c < len(a):
        ret = fs.event(a[c])
        # Make sure a transition back to start (from something else) does not consume the character.
        if ret[0] != "Start" or (ret[0] == "Start" and ret[1] == False):
            c += 1
    ret = fs.event("")

    print t.tokenList
