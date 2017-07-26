#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -----------------------------------------------------------------------------
# Event and EventDispatcher classes
# -----------------------------------------------------------------------------
    
class Event( object ):
    """
    Generic event to use with EventDispatcher.
    """
    
    def __init__(self, event_type, data=None):
        """
        The constructor accepts an event type as string and a custom data
        """
        self._type = event_type
        self._data = data
        
    @property 
    def type(self):
        """
        Returns the event type
        """
        return self._type
        
    @property
    def data(self):
        """
        Returns the data associated to the event
        """
        return self._data


class EventDispatcher( object ):
    """
    Generic event dispatcher which listen and dispatch events
    """
    
    def __init__(self):
        self._events = dict()
        
    def __del__(self):
        """
        Remove all listener references at destruction time
        """
        self._events = None
    
    def has_listener(self, event_type, listener):
        """
        Return true if listener is register to event_type
        """
        # Check for event type and for the listener
        if event_type in self._events.keys():
            return listener in self._events[ event_type ]
        else:
            return False
        
    def dispatch_event(self, event):
        """
        Dispatch an instance of Event class
        """
        # Dispatch the event to all the associated listeners 
        if event.type in self._events.keys():
            listeners = self._events[ event.type ]
            
            for listener in listeners:
                listener( event )
        
    def add_event_listener(self, event_type, listener):
        """
        Add an event listener for an event type
        """
        # Add listener to the event type
        if not self.has_listener( event_type, listener ):
            listeners = self._events.get( event_type, [] )
        
            listeners.append( listener )
            
            self._events[ event_type ] = listeners
    
    def remove_event_listener(self, event_type, listener):
        """
        Remove event listener.
        """
        # Remove the listener from the event type
        if self.has_listener( event_type, listener ):
            listeners = self._events[ event_type ]
            
            if len( listeners ) == 1:
                # Only this listener remains so remove the key
                del self._events[ event_type ]
                
            else:
                # Update listeners chain
                listeners.remove( listener )
                
                self._events[ event_type ] = listeners


# ------------------------------------------------------------------------------
# Events and Dispatcher example
#
# In this example we create a simple event MyEvent with only two event types,
# ASK and RESPOND, and two classes: WhoAsk, which send AKS event and listen for
# the RESPOND event, and WhoRespond, which listen for ASK events and send back
# a RESPOND event
# -----------------------------------------------------------------------------

class MyEvent( Event ):
    """
    When subclassing Event class the only thing you must do is to define
    a list of class level constants which defines the event types and the 
    string associated to them
    """
    
    ASK     = "askMyEvent"
    RESPOND = "respondMyEvent"


class WhoAsk( object ):
    """
    First class which ask who is listening to it
    """
    def __init__(self, event_dispatcher):
        # Save a reference to the event dispatch
        self.event_dispatcher = event_dispatcher
        
        # Listen for the RESPOND event type
        self.event_dispatcher.add_event_listener( 
            MyEvent.RESPOND, self.on_answer_event 
        )
        
    def ask(self):
        """
        Dispatch the ask event
        """
        print ">>> I'm instance {0}. Who are listening to me ?".format( self )

        self.event_dispatcher.dispatch_event( 
            MyEvent( MyEvent.ASK, self ) 
        )
        
    def on_answer_event(self, event):
        """
        Event handler for the RESPOND event type
        """
        print "<<< Thank you instance {0}".format( event.data )
        

class WhoRespond( object ):
    """
    Second class who respond to ASK events
    """
    def __init__(self, event_dispatcher):
        # Save event dispatcher reference
        self.event_dispatcher = event_dispatcher
        
        # Listen for ASK event type
        self.event_dispatcher.add_event_listener( 
            MyEvent.ASK, self.on_ask_event 
        )
        
    def on_ask_event(self, event):
        """
        Event handler for ASK event type
        """
        self.event_dispatcher.dispatch_event( 
            MyEvent ( MyEvent.RESPOND, self ) 
        )


if __name__ == "__main__":
    # Create and instance of event dispatcher
    dispatcher = EventDispatcher()
    
    # Create an instance of WhoAsk class and two instance of WhoRespond class
    who_ask = WhoAsk( dispatcher )
    who_responde1 = WhoRespond( dispatcher )
    who_responde2 = WhoRespond( dispatcher )
    
    # WhoAsk ask :-)
    who_ask.ask()
