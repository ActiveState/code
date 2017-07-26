"""
    Transactions of attributes by inheriting the Transaction class

    Basic Usage:
    
    class Test(Transaction):
        pass
        
    a = Test()
    a.test = "old state"
    a.commit()
    a.test = "bad state, roll me back"
    a.rollback()
    assert(a.test == "old state")
    
 See also: http://www.harald-hoyer.de/linux/pythontransactionclass
 
 Copyright (C) 2008 Harald Hoyer <harald@redhat.com>
 Copyright (C) 2008 Red Hat, Inc.
"""

import copy

def _checksetseen(what, seen):
    "checks and sets the obj id in seen"
    if what in seen:
        return True
    seen.add(what)
    return False

class Transaction(object):
    """
    This class allows sub-classes to commit changes to an instance to a 
    history, and rollback to previous states.
        
    Because the class only stores attributes in self.__dict__ sub-classes
    need to use the methods __getstate__ and __setstate__ to provide additional
    state information. See the Transactionlist below for an example usage.    
    """

    def commit(self, **kwargs):
        """
        Commit the object state.
        
        If the optional argument "deep" is set to False,
        objects of class Transaction stored in this object will
        not be committed.
        """
        seen = kwargs.get("_commit_seen", set())
        if _checksetseen(id(self), seen): 
            return
        deep = kwargs.get("deep", True)
        
        # Do not deepcopy the Transaction objects. We want to keep the 
        # reference. Instead commit() them.     
        state = dict()
        for key, val in self.__dict__.items():
            if isinstance(val, Transaction):
                state[key] = val
                if deep:
                    val.commit(_commit_seen = seen)
            elif key == "__l":
                # do not deepcopy our old state
                state[key] = val
            else:
                state[key] = copy.deepcopy(val)
                
        if hasattr(self, '__getstate__'):            
            state = (state, getattr(self, '__getstate__')())

        self.__dict__["__l"] = state
                
    def rollback(self, **kwargs):
        """
        Rollback the last committed object state.
        
        If the optional argument "deep" is set to False,
        objects of class Transaction stored in this object will
        not be rolled back.
        """
        seen = kwargs.get("_rollback_seen", set())
        if _checksetseen(id(self), seen):
            return
        
        deep = kwargs.get("deep", True)
        state = None
        extrastate = None
        gotstate = False
        gotextrastate = False
        if "__l" in self.__dict__:
            state = self.__dict__["__l"]
            gotstate = True
            if type(state) is tuple:
                gotextrastate = True
                (state, extrastate) = state

        # rollback our childs, then ourselves
        for child in self.__dict__.values():
            if isinstance(child, Transaction):
                if deep:
                    child.rollback(_rollback_seen = seen)
 
        if gotstate:
            self.__dict__.clear()
            self.__dict__.update(state)
            
        if gotextrastate and hasattr(self, '__setstate__'):
            getattr(self, '__setstate__')(extrastate)


class Transactionlist(list, Transaction):
    """
    An example subclass of list, which inherits transactions.
    
    Due to the special list implementation, we need the 
    __getstate__ and __setstate__ methods.
    
    See the code for the implementation.
    """
    def commit(self, **kwargs):
        """
        Commit the object state.
        
        If the optional argument "deep" is set to False,
        objects of class Transaction stored in this object will
        not be committed.
        """
        # make a local copy of the recursive marker
        seen = set(kwargs.get("_commit_seen", set()))
        
        super(Transactionlist, self).commit(**kwargs)

        if _checksetseen(id(self), seen): 
            return
        
        deep = kwargs.get("deep", True)
        if deep:
            for val in self:
                if isinstance(val, Transaction):
                    val.commit()
        
    def rollback(self, **kwargs):
        """
        Rollback the last committed object state.
        
        If the optional argument "deep" is set to False,
        objects of class Transaction stored in this object will
        not be rolled back.
        """
        # make a local copy of the recursive marker
        seen = set(kwargs.get("_rollback_seen", set()))

        super(Transactionlist, self).rollback(**kwargs)

        if _checksetseen(id(self), seen):
            return
        
        deep = kwargs.get("deep", True)
        if deep:
            for val in self:
                if isinstance(val, Transaction):
                    val.rollback()

                
    def __getstate__(self):
        """
        return a deepcopy of all non Transaction class objects in our list, 
        and a reference for the committed Transaction objects.
        
        """
        state  = []
        for val in self:
            if isinstance(val, Transaction):
                state.append(val)
            else:
                state.append(copy.deepcopy(val))
                
        return state        

    def __setstate__(self, state):
        "clear the list and restore all objects from the state"
        del self[:]
        self.extend(state)

__author__ = "Harald Hoyer <harald@redhat.com>"
