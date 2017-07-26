def statemethod(method):
    def call_statemethod(self, *args, **kwargs):
        # Use self.state.<method> if available, else method itself.
        real_method = getattr(self.state, method.func_name, method)
        return real_method(self, *args, **kwargs)
    call_statemethod.default = method
    return call_statemethod


# Sample usage:
class State(object):
    """Base State class, direct parent to non-instantiated states.

       Useful when you have lots of base objects and don't need to store
       per-state data."""

    @classmethod
    def new(cls):
        """Create a new Base object with this as the initial state."""
        return Base(cls.get_state())

    @classmethod
    def get_state(cls):
        """Get the state, for use with an existing Base object"""
        return cls

class InstantiatedState(State):
    """InstantiatedState creates a new object every time get_state is called.

       This allows for independant per-state data storage by multiple base
       objects."""

    @classmethod
    def get_state(cls):
        """Get a state object, for use with an existing Base object"""
        return cls()

class Base(object):
    def __init__(self, initial_state):
        self.state = initial_state

    def ordinary_method(self):
        print "This method is ordinary."

    @statemethod
    def default_method(self):
        print "This is a default method that has not been overridden."

    @statemethod
    def overridden_method(self):
        print "You shouldn't see this."
        assert False

class SimpleState(State):
    @staticmethod
    def overridden_method(base):
        print "The method on %r has been overridden by SimpleState." % base

class DataState(InstantiatedState):
    message = "Awesome."
    def overridden_method(self, base):
        print "This method on %r has been overridden by DataState.  %s" \
                          % (base,                            self.message)

print "Base A"
print "======"
base_a = SimpleState.new()
print "Calling default_method:"
base_a.default_method()
print "Calling overridden_method:"
base_a.overridden_method()
print "Switching to DataState."
base_a.state = DataState.get_state()
print "Calling overridden_method:"
base_a.overridden_method()
print "Changing message."
base_a.state.message = "Excellent."
print "Calling overridden_method:"
base_a.overridden_method()
print
print "Base B"
print "======"
base_b = DataState.new()
print "Calling default_method:"
base_b.default_method()
print "Calling overridden_method:"
base_b.overridden_method()
