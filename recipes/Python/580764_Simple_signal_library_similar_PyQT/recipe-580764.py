import contextlib

__all__ = ["Signal", "SignalFactory", "NotRregisteredSignal", "InvalidSlot"]

class InvalidSlot(Exception):
    """Slot is not longer valid"""

class NotRregisteredSignal(ValueError):
    """Signal not registered in factory beforehand"""

class Slot(object):
    """Base class of slots"""
    def __init__(self, signal, func, max_calls=None):
        if not callable(func):
            raise ValueError("objects is not non-callable")

        self._signal = signal
        self._max_calls = max_calls

        self._func = func

    @property
    def func(self):
        return self._func

    @property
    def signal(self):
        return self._signal

    @property
    def max_calls(self):
        return self._max_calls

    def __call__(self, *args, **kwargs):
        if self._max_calls is not None:
            if self._max_calls == 0:
                raise InvalidSlot("Not possible to call more times callback")
            else:
                self._max_calls -= 1
            
        self._func(*args, **kwargs)
    
class Signal(object):
    """The Signal is the core object that handles connection and emission ."""

    def __init__(self, name=""):
        self._blocked = False
        self._slots = []

        self._name = str(name)
        
    @property
    def name(self):
        return self._name

    def emit(self, *args, **kwargs):
        """Calls all the connected slots with the provided args and kwargs unless block is activated"""

        if self._blocked: return

        for slot_index, slot in enumerate(list(self._slots)):
            slot(*args, **kwargs)
            
            if slot.max_calls == 0:
                del self._slots[slot_index]

    def on(self, callback, max_calls=None):
        if not callable(callback):
            raise ValueError("Connection to non-callable object failed")
        
        if max_calls is not None and not isinstance(max_calls, int):
            raise ValueError("max_calls should be None or integer")
            
        slot = Slot(self, callback, max_calls)
        self._slots.append(slot)
        
        return slot
    
    def once(self, callback):
        """Registers a callback that will respond to an event at most one time"""

        return self.on(callback, max_calls=1, weak_ref=weak_ref)

    def disconnect(self, slot):
        """Disconnects the slot from the signal"""

        """
        if not isinstance(slot, Slot):
            raise ValueError("Arguments is not slot")
        """
        if slot.signal != self: return

        found = False
        for index, other_slot in enumerate(self._slots):
            if other_slot == slot:
                found = True
                break

        if not found:
            raise Exception("Not valid slot.")
        
        del self._slots[index]

    def clear(self):
        """Clears the signal of all connected slots"""

        self._slots = []

    def block(self, isBlocked):
        """Sets blocking of the signal"""

        self._blocked = bool(isBlocked)
    
    @property    
    def is_blocked(self):
        return self._blocked
        
    @property
    def number_of_slots(self):
        return len(self._slots)

class Signal_Factory(object):
    """The Signal Factory object lets you handle signals by a string based name instead of by objects."""

    def __init__(self, mandatory_registry=False):
        self._signal_registry = dict()
        self._mandatory_registry = mandatory_registry

    def _check_signal_is_registered(self, signal):
        if signal not in self._signal_registry:
            if self._mandatory_registry:
                raise NotRregisteredSignal
            else:
                self._signal_registry[signal] = Signal(name=signal)

    def add_signal(self, signal_obj):
        self._signal_registry[signal_obj.name] = signal_obj
        
    def register_signal(self, signal):
        if signal in self._signal_registry:
            raise ValueError("Signal already registered")

        self._signal_registry[signal] = Signal()
        
    def unregister_signal(self, signal):
        if signal not in self._signal_registry:
            raise ValueError("Not posisble to unregistered not registered signal: %s"%signal)
        
        self._signal_registry[signal].clear()
        del self._signal_registry[signal]

    def signal_names(self):
        return self._signal_registry.keys()

    def emit(self, signal, *args, **kwargs):
        """Emits a signal by name. Any additional args or kwargs are passed to the signal"""

        self._check_signal_is_registered(signal)
        self._signal_registry[signal].emit(*args, **kwargs)

    def on(self, signal, callback=None, max_calls=None):
        """
        Registers a single callback for receiving an event. Optionally, can specify a maximum number 
        of times the callback should receive a signal. This method works as both a function and a decorator.
        """
        
        self._check_signal_is_registered(signal)

        if callback is None:
            # decorator
            def decorator(callback):
                self.on(signal, callback, max_calls=max_calls)
                
            return decorator
        else:
            return self._signal_registry[signal].on(callback, max_calls=max_calls)
        
    def once(self, signal, callback=None, weak_ref=True):
        self._check_signal_is_registered(signal)

        if callback is None:
            # decorator
            def decorator(callback):
                return self.once(signal, callback, max_calls=max_calls)
                
            return decorator
        else:
            return self._signal_registry[signal].once(callback)

    def block(self, signal=None, isBlocked=True):
        """Sets the block on provided signals, or to all signals"""

        if signal is None:
            for signal in self._signal_registry.keys():
                self._signal_registry[signal].block(isBlocked)
        else:
            self._check_signal_is_registered(signal)

            self._signal_registry[signal].block(isBlocked)
        
    def unblock(self, signal=None):
        if signal is None:
            for signal in self._signal_registry.keys():
                self._signal_registry[signal].block(False)
        else:
            self._check_signal_is_registered(signal)

            self._signal_registry[signal].block(False)
        
    def is_blocked(self, signal):
        self._check_signal_is_registered(signal)

        return self._signal_registry[signal].is_blocked()

    def disconnect_from(self, signal, slot):
        """Remove slot from receiver list if it responds to the signal"""
        
        self._check_signal_is_registered(signal)
        self._signal_registry[signal].disconnect(slot)

    def disconnect(self, slot):
        if not isinstance(slot, Slot):
            raise ValueError("Argument not a slot")

        self._signal_registry[slot.signal.name].disconnect(slot)
    
    def clear_all(self):
        """
        Clears all callbacks for all signals
        """
        for signal_object in self._signal_registry.values():
            signal_object.clear()
            
    def clear(self, *signals):
        """Clears all callbacks for a particular signal or signals"""

        if signals:
            for signal in signals:
                self._check_signal_is_registered(signal)
        else:
            signals = self._signal_registry.keys()

        for signal in signals:
            self._signal_registry[signal].clear()

    @contextlib.contextmanager
    def emitting(self, exit, enter=None):
        """
        Context manager for emitting signals either on enter or on exit of a context.
        By default, if this context manager is created using a single arg-style argument,
        it will emit a signal on exit. Otherwise, keyword arguments indicate signal points
        """
        
        self._check_signal_is_registered(exit)

        if enter is not None:
            self._check_signal_is_registered(enter)
            self.emit(enter)

        try:
            yield
        finally:
            self.emit(exit)
    
    def signal(self, signal):
        self._check_signal_is_registered(signal)
        return self._signal_registry[signal]

    def __contains__(self, signal):
        return signal in self._signal_registry
        
    exists_signal = __contains__

    def number_of_slots(self, signal):
        if signal in self._signal_registry:
            return self._signal_registry[signal].number_of_slots
        else:
            raise NotRregisteredSignal

    def __getitem__(self, signal):
        return self._signal_registry[signal]

    def __delitem__(self, signal):
        del self._signal_registry[signal]

if __name__ == "__main__":
    def greet1(name):
        print("Hello,", name)
        
    def greet2(name):
        print("Hi,", name)

    connection = Signal_Factory()
    connection.on('Greet', greet1)
    slot = connection.on('Greet', greet2)

    connection.emit('Greet', "John")

    connection.disconnect_from("Greet", slot)
    connection.emit('Greet', "Albert")
    
    print("------------------")
    connection.clear('Greet')
    
    print ("Greet has %d slots"%connection.signal("Greet").number_of_slots)
    slot = connection.on('Greet', greet2)
    # It's possible to disconnect directly without indicating the name of signal.
    connection.disconnect(slot)

    print("No output because there is no handler..")
    connection.emit('Greet', "Albert")
    
    print("------------------")
    connection2 = Signal_Factory()
    
    @connection2.on('foo')
    def my_callback1():
        print("called my_callback1()")

    @connection2.on('foo', max_calls=2)
    def my_callback2():
        print("called my_callback2()")
        
    with connection2.emitting('foo'):
        print("inside first with statement")
        
    print("------------------")
    
    def exit_func():
        print("exit of context manager")

    connection2.on('bar', exit_func)

    # 'foo' emitted on enter, 'bar' emitted on exit
    with connection2.emitting(enter='foo', exit='bar'):
        print("inside second with statement")
