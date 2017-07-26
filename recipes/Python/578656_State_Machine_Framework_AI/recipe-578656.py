from time import sleep
from random import randint, shuffle

class StateMachine(object):
    ''' Usage:  Create an instance of StateMachine, use set_starting_state(state) to give it an
        initial state to work with, then call tick() on each second (or whatever your desired
        time interval might be. '''

    def set_starting_state(self, state):
        ''' The entry state for the state machine. '''
        state.enter()
        self.state = state
        
    def tick(self):
        ''' Calls the current state's do_work() and checks for a transition '''
        next_state = self.state.check_transitions()
        
        if next_state is None:
            # Stick with this state
            self.state.do_work()
        else:
            # Next state found, transition to it
            self.state.exit()
            next_state.enter()
            self.state = next_state
        
    
class BaseState(object):
    ''' Usage: Subclass BaseState and override the enter(), do_work(), and exit() methods. 
        
            enter()    -- Setup for your state should occur here.  This likely includes adding 
                          transitions or initializing member variables.
                       
            do_work()  -- Meat and potatoes of your state.  There may be some logic here that will
                          cause a transition to trigger.
                          
            exit()     -- Any cleanup or final actions should occur here.  This is called just
                          before transition to the next state.
    '''
    
    def add_transition(self, condition, next_state):
        ''' Adds a new transition to the state.  The "condition" param must contain a callable
            object.  When the "condition" evaluates to True, the "next_state" param is set as
            the active state. '''
        # Enforce transition validity
        assert(callable(condition))
        assert(hasattr(next_state, "enter"))
        assert(callable(next_state.enter))
        assert(hasattr(next_state, "do_work"))
        assert(callable(next_state.do_work))
        assert(hasattr(next_state, "exit"))
        assert(callable(next_state.exit))
        
        # Add transition
        if not hasattr(self, "transitions"):
            self.transitions = []
        self.transitions.append((condition, next_state))

    def check_transitions(self):
        ''' Returns the first State thats condition evaluates true (condition order is randomized) '''
        if hasattr(self, "transitions"):
            shuffle(self.transitions)
            for transition in self.transitions:
                condition, state = transition
                if condition():
                    return state

    def enter(self):
        pass
        
    def do_work(self):
        pass
        
    def exit(self):
        pass


##################################################################################################
############################### EXAMPLE USAGE OF STATE MACHINE ###################################
##################################################################################################
class WalkingState(BaseState):
    def enter(self):
        print("WalkingState: enter()")
        def condition(): return randint(1, 5) == 5
        self.add_transition(condition, JoggingState())
        self.add_transition(condition, RunningState())
        
    def do_work(self):
        print("Walking...")
        
    def exit(self):
        print("WalkingState: exit()")
        
        
class JoggingState(BaseState):
    def enter(self):
        print("JoggingState: enter()")
        self.stamina = randint(5, 15)
        def condition(): return self.stamina <= 0
        self.add_transition(condition, WalkingState())
        
    def do_work(self):
        self.stamina -= 1
        print("Jogging ({0})...".format(self.stamina))
        
    def exit(self):
        print("JoggingState: exit()")
        
        
class RunningState(BaseState):
    def enter(self):
        print("RunningState: enter()")
        self.stamina = randint(5, 15)
        def walk_condition(): return self.stamina <= 0
        self.add_transition(walk_condition, WalkingState())
        
        def trip_condition(): return randint(1, 10) == 10
        self.add_transition(trip_condition, TrippingState())
        
    def do_work(self):
        self.stamina -= 2
        print("Running ({0})...".format(self.stamina))
        
    def exit(self):
        print("RunningState: exit()")
        
        
class TrippingState(BaseState):
    def enter(self):
        print("TrippingState: enter()")
        self.tripped = False
        def condition(): return self.tripped
        self.add_transition(condition, WalkingState())
        
    def do_work(self):
        print("Tripped!")
        self.tripped = True
        
    def exit(self):
        print("TrippingState: exit()")
        

if __name__ == "__main__":
    state = WalkingState()
    
    state_machine = StateMachine()
    state_machine.set_starting_state(state)
    
    while True:
        state_machine.tick()
        sleep(1)
