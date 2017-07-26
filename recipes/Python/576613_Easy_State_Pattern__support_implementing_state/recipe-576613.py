"""
Supports implementation of state pattern.

State Machine is defined a class containing one or more StateTable objeects, 
and using decorators to define Events and Transitions that are handled by the 
state machine.  Individual states are Subclasses of the state machine, with 
a __metaclass__ specifier.

Author: Rodney Drenth
Date:   January, 2009
Version: Whatever

Copyright 2009, Rodney Drenth

Permission to use granted under the terms and conditions of the Python Software
Foundation License
 (http://www.python.org/download/releases/2.4.2/license/)

"""
#! /usr/bin/env Python
#

import types

class _StateVariable( object ):
   """Used as attribute of a class to maintain state.

      State Variable objects are not directly instantiated in the user's state machine class
      but are instantiated by the StateTable class attribute defined within the state machine.
   """

   def __init__(self, stateTable):
      """ Constructs state variable and sets it to the initial state
      """
      self._current_state = stateTable.initialstate
      self._next_state = stateTable.initialstate
      self.sTable = stateTable

   def _toNextState(self, context):
      """Sets state of to the next state, if new state is different. 
      calls onLeave and onEnter methods
      """
      if self._next_state is not self._current_state:
         if hasattr(self._current_state, 'onLeave'):
            self._current_state.onLeave(context)
         self._current_state = self._next_state
         if hasattr(self._current_state, 'onEnter'):
            self._current_state.onEnter(context)

   def name(self):
      """Returns ame of current state."""
      return self._current_state.__name__

   def setXition(self, func):
      """ Sets the state to transitionto upon seeing Transition event"""
#      next_state = self.sTable.nextStates[self._current_state][func.__name__]
      next_state = self._current_state.nextStates[func.__name__]
      if next_state is not None:
         self._next_state = next_state

   def getFunc(self, func):
      """ Gets event handler function based on current State"""
      funky = getattr( self._current_state, func.__name__)
#      print 'current State:', self._current_state.__name__
      if funky is None:
         raise NotImplementedError('%s.%s'%(self.name(),func.__name__))

      # when funky.name is objCall, it means that we've recursed all the
      # way back to the context class and need to call func as a default
      return funky if funky.__name__ != 'objCall' else func


class StateTable( object ):
   """Defines a state table for a state machine class

   A state table for a class is associated with the state variable in the instances
   of the class. The name of the state variable is given in the constructor to the 
   StateTable object.  StateTable objects are attributes of state machine classes, 
   not intances of the state machine class.   A state machine class can have more
   than one StateTable.
   """

   def __init__(self, stateVarblName):
      """State Table initializer

      stateVarblName is the name of the associated state variable, which will
      be instantiated in each instance of the state machine class
      """
      self.inst_state_name = stateVarblName
      self.eventList = []
      self.initialstate = None
      nextStates = {}

   def initialize(self, obj ):
      """Initialization of StateTable and state varible

      obj is the instance of the state machine being initialized. This method
      must be called in the __init__ method of the user's state machine.
      """
      obj.__dict__[self.inst_state_name] = _StateVariable( self )

   def _addEventHandler(self, funcName):
      """Notifies State table of a method that's handle's an transition.

      This is called by @Transition and @TransitionEvent decorators,
      whose definitions are below.
      """
      self.eventList.append(funcName)

   def nextStates(self, subState, nslList):
      """Sets up transitions from the state specified by subState

      subState is a state class, subclassed from user's state machine class
      nslList is a list of states that will be transitioned to upon Transitions.
      This functions maps each @Transition decorated method in the state machine
      class to a to the corresponding state in this list.  None can be specified
      as a state to indicate the state should not change.
      """
      if len(nslList) != len(self.eventList):
         raise RuntimeError( "Wrong number of states in transition list.")
      subState.nextStates = dict(zip(self.eventList, nslList))
#      self.nextStates[subState] = dict(zip( self.eventList, nslList))

def Event( state_table ):
   """Decorator for indicating state dependant method

   Decorator is applied to methods of state machine class to indicate that
   invoking the method will call state dependant method.   States are implemented
   as subclasses of the state machine class with a metaclass qualification.
   """
   stateVarName = state_table.inst_state_name

   def wrapper(func):
      # no adding of event handler to statetable...
      def objCall( self, *args, **kwargs):
         state_var = getattr(self, stateVarName )
         retn = state_var.getFunc(func)(self, *args, **kwargs)
         return retn

      return objCall
   return wrapper


def Transition( state_table ):
   """Decorator for indicating the method causes a state transition.

   Decorator is applied to methods of the state machine class. Invokeing
   the method can cause a transition to another state.  Transitions are defined
   using the nextStates method of the StateTable class
   """
   stateVarName = state_table.inst_state_name

   def wrapper(func):
      state_table._addEventHandler( func.__name__)

      def objCall( self, *args, **kwargs):
         state_var = getattr(self, stateVarName )
         state_var.setXition(func)
         rtn = func(self, *args, **kwargs)
         state_var._toNextState(self)
         return  rtn

      return objCall
   return wrapper


def TransitionEvent( state_table ):
   """Decorator for defining a method that both triggers a transition and
   invokes a state dependant method.

   This is equivalent to, but more efficient than using
   @Transition(stateTable)
   @Event(stateTable)
   """
   stateVarName = state_table.inst_state_name

   def wrapper(func):
      state_table._addEventHandler( func.__name__)

      def objCall( self, *args, **kwargs):
         state_var = getattr(self, stateVarName )
#         if not issubclass( state_var._current_state, self.__class__):
#            raise TypeError('expecting instance to be derived from %s'% baseClasss.__name__)
         state_var.setXition(func)
         retn = state_var.getFunc(func)(self, *args, **kwargs)
         state_var._toNextState(self)
         return retn

      return objCall
   return wrapper


class _stateclass(type):
   """ A stateclass metaclass 
   
   Modifies class so its subclass's methods so can be called as methods
   of a base class. Is used for implementing states
   """

   def __init__(self, name, bases, cl_dict):
      self.__baseClass__ = _bcType              # global - set by stateclass(), which follows
      if not issubclass(self, _bcType):
         raise TypeError( 'Class must derive from %s'%_bcType.__name__ )
      type.__init__(self, name, bases, cl_dict)

   def __getattribute__(self, name):
      if name.startswith('__'):
            return type.__getattribute__(self, name)
      try:
         atr = self.__dict__[name]
         if type(atr) == types.FunctionType:
            atr = types.MethodType(atr, None, self.__baseClass__)
      except KeyError, ke:
         for bclas in self.__bases__:
            try:
               atr = getattr(bclas, name)
               break
            except AttributeError, ae:
               pass
         else:
            raise AttributeError( "'%s' has no attribute '%s'" % (self.__name__, name) )
      return atr


def stateclass( statemachineclass ):
   """A method that returns a metaclass for constructing states of the
   users state machine class
   """
   global _bcType
   _bcType = statemachineclass
   return _stateclass

#  vim : set ai sw=3 et ts=6 :
-----------------------------------------------------------
"""
Example of setting up a state machine using the EasyStatePattern
module.
"""
import EasyStatePattern as esp
import math


class Parent(object):
    """ the context for the state machine class """
    moodTable = esp.StateTable('mood')

    def __init__(self, pocketbookCash, piggybankCash):
      """Instance initializer must invoke the initialize method of the StateTable """
      Parent.moodTable.initialize( self)
      self.pocketBook = pocketbookCash
      self.piggyBank = piggybankCash

    """The Transiton decorator defines a method which causes transitions to other
    states"""
    @esp.Transition(moodTable)
    def getPromotion(self): pass

    @esp.Transition(moodTable)
    def severalDaysPass(self): pass


    """The Event decorator defines a method whose exact method will depend on the
    current state. These normally do not cause a state transition.
    For this example, this method will return an amount of money that the asker is to receive,
    which will depend on the parent's mood, the amount asked for, and the availability of
    money."""
    @esp.Event(moodTable)
    def askForMoney(self, amount): pass

    """The TransitionEvent decorator acts like a combination of both the Transition
    and Event decorators.  Calling this causes a transition(if defined in the state
    table) and the called function is state dependant."""
    @esp.TransitionEvent(moodTable)
    def cashPaycheck(self, amount): pass

    @esp.TransitionEvent(moodTable)
    def getUnexpectedBill(self, billAmount ): pass

    """onEnter is called when entering a new state. This can be overriden in
    the individual state classes.  onLeave (not defined here) is called upon
    leaving a state"""
    def onEnter(self):
      print 'Mood is now', self.mood.name()

# 
# Below are defined the states. Each state is a class, States may be derived from
# other states. Topmost states must have a __metaclass__ = stateclass( state_machine_class )
# declaration.
#
class Normal( Parent ):
    __metaclass__ = esp.stateclass( Parent )
    """Normal becomes the name of the state."""

    def getPromotion(self): 
        """This shouldn't get called, since get was defined as a transition in
        the Parent context"""
        pass

    def severalDaysPass(self): 
       """neither should this be called."""
       pass

    def askForMoney(self, amount): 
        amountToReturn = min(amount, self.pocketBook )
        self.pocketBook -= amountToReturn
        if  40.0 < self.pocketBook:
            print 'Here you go, sport!'
        elif 0.0 < self.pocketBook < 40.00:
            print "Money doesn't grow on trees, you know."
        elif 0.0 < amountToReturn < amount:
            print "Sorry, honey, this is all I've got."
        elif amountToReturn == 0.0:
            print "I'm broke today ask your aunt."
            self.mood.nextState = Broke
        return amountToReturn

    def cashPaycheck(self, amount): 
        self.pocketBook += .7 * amount
        self.piggyBank += .3*amount

    def getUnexpectedBill(self, billAmount ): 
        amtFromPktBook = min(billAmount, self.pocketBook)
        rmngAmt = billAmount - amtFromPktBook
        self.piggyBank -= rmngAmt
        self.pocketBook -= amtFromPktBook
        

class Happy( Parent ):
    __metaclass__ = esp.stateclass( Parent )
    """Grouchy becomes the name of the state."""

    def askForMoney(self, amount): 
        availableMoney = self.pocketBook + self.piggyBank
        amountToReturn = max(min(amount, availableMoney), 0.0)
        amountFromPktbook =  min(amountToReturn, self.pocketBook)
        self.pocketBook -= amountFromPktbook
        self.piggyBank -= (amountToReturn - amountFromPktbook)

        if 0.0 < amountToReturn < amount:
            print "Sorry, honey, this is all I've got."
        elif amountToReturn == 0.0:
            print "I'm broke today ask your aunt."
            self.mood.nextState = Broke
        else:
            print 'Here you go, sport!'
        return amountToReturn

    def cashPaycheck(self, amount): 
        self.pocketBook += .75 * amount
        self.piggyBank += .25*amount

    def getUnexpectedBill(self, billAmount ): 
        print "why do these things always happen?"
        amtFromPktBook = min(billAmount, self.pocketBook)
        rmngAmt = billAmount - amtFromPktBook
        self.piggyBank -= rmngAmt
        self.pocketBook -= amtFromPktBook
        
    def onEnter(self):
      print 'Yippee! Woo Hoo!', self.mood.name()*3

class Grouchy( Parent ):
    __metaclass__ = esp.stateclass( Parent )
    """Grouchy becomes the name of the state."""

    def askForMoney(self, amount): 
       print """You're always spending too much. """
       return 0.0

    def cashPaycheck(self, amount): 
        self.pocketBook += .70 * amount
        self.piggyBank += .30*amount

    def getUnexpectedBill(self, billAmount ): 
        print 'These things always happen at the worst possible time!'

        amtFromPktBook = min(billAmount, self.pocketBook)
        rmngAmt = billAmount - amtFromPktBook
        self.piggyBank -= rmngAmt
        self.pocketBook -= amtFromPktBook
        

class Broke( Normal ):
    #   __metaclass__ = esp.stateclass( Parent )
    """ No metaclass declaration as its as subclass of Grouchy. """

    def cashPaycheck(self, amount): 
        piggyBankAmt = min ( amount, max(-self.piggyBank, 0.0))
        rmngAmount = amount - piggyBankAmount
        self.pocketBook += .40 * rmngAmount
        self.piggyBank += (.60 * rmngAmount + piggyBankAmt)

    def askForMoney(self, amount): 
        amountToReturn = min(amount, self.pocketBook )
        self.pocketBook -= amountToReturn
        if  40.0 < self.pocketBook:
            print 'Here you go, sport!'
        elif 0.0 < self.pocketBook < 40.00:
            print "Spend it wisely."
        elif 0.0 < amountToReturn < amount:
            print "This is all I've got."
        elif amountToReturn == 0.0:
            print "Sorry, honey, we're broke."
            self.mood.nextState = Broke
        return amountToReturn


# After defining the states, The following lines set up the transitions.
# We've set up four transitioning methods, 
# getPromotion, severalDaysPass, cashPaycheck, getUnexpectedBill 
# Therefore there are four states in each list, the ordering of the states in the
# list corresponds toorder that the transitioning methods were defined.

Parent.moodTable.nextStates( Normal, ( Happy, Normal, Normal, Grouchy ))
Parent.moodTable.nextStates( Happy, ( Happy, Happy, Happy, Grouchy ))
Parent.moodTable.nextStates( Grouchy, ( Happy, Normal, Grouchy, Grouchy ))
Parent.moodTable.nextStates( Broke, ( Normal, Broke, Grouchy, Broke ))

# This specifies the initial state. Instances of the Parent class are placed
# in this state when they are initialized.
Parent.moodTable.initialstate = Normal


def Test():
    dad = Parent(50.0, 60.0)
    amount = 20.0
    print amount, dad.askForMoney(amount)
    print amount, dad.askForMoney(amount)
    dad.cashPaycheck( 40.0)
    print amount, dad.askForMoney(amount)
    dad.cashPaycheck( 40.0)
    dad.severalDaysPass()
    print amount, dad.askForMoney(amount)
    dad.getUnexpectedBill(100.0 )
    print amount, dad.askForMoney(amount)
    dad.severalDaysPass()
    print amount, dad.askForMoney(amount)
    dad.severalDaysPass()
    dad.cashPaycheck( 100.0)
    print amount, dad.askForMoney(amount)
    dad.cashPaycheck( 50.0)
    print amount, dad.askForMoney(amount)
    dad.getPromotion()
    dad.cashPaycheck( 200.0)
    amount = 250
    print amount, dad.askForMoney(amount)

Test()
