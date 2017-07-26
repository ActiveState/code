##
# This module provides a powerful 'switch'-like dispatcher system.
# Values for switch cases can be anything comparable via '==', a string
# for use on the left-hand side of the 'in' operator, or a regular expression.
# Iterables of these types can also be used.

__author__ = 'Mike Kent'

import re

class SwitchError(Exception): pass

CPAT_TYPE = type(re.compile('.'))
STR_TYPE = type('')
LIST_TYPE = type([])
TUPLE_TYPE = type(())

class Switch(object):
    
    def __init__(self):
        self.exactCases = {}
        self.inCases = []
        self.patternCases = []
        self.defaultHandler = None
        
    ##
    # Try each 'in' case, in the order they were
    # specified, stopping if we get a match.
    # Return a tuple of the string we are searching for in the target string,
    # and the case handler found, or (None, None) if no match found.
    def _findInCase(self, switchValue):
        for inStr, aHandler in self.inCases:
            if inStr in switchValue:
                return (inStr, aHandler)
        return (None, None)
    
    ##
    # Try each regex pattern (using re.search), in the order they were
    # specified, stopping if we get a match.
    # Return a tuple of the re match object and the case handler found, or
    # (None, None) if no match found.
    def _findRegExCase(self, switchValue):
        for cpat, aHandler in self.patternCases:
            matchObj = cpat.search(switchValue)
            if matchObj is not None:
                return (matchObj, aHandler)
        return (None, None)
        
    ##
    # Switch on a switch value.  A match against the exact
    # (non-regular-expression) case matches is tried first.  If that doesn't
    # find a match, then if the switch value is a string, the 'in' case
    # matches are tried next, in the order they were registered.  If that
    # doesn't find a match, then if the switch value is a string,
    # the regular-expression case matches are tried next, in
    # the order they were registered.  If that doesn't find a match, and
    # a default case handler was registered, the default case handler is used.
    # If no match was found, and no default case handler was registered,
    # SwitchError is raised.
    # If a switch match is found, the corresponding case handler is called.
    # The switch value is passed as the first positional parameter, along with
    # any other positional and keyword parameters that were passed to the
    # switch method.  The switch method returns the return value of the
    # called case handler.
    
    def switch(self, switchValue, *args, **kwargs):

        caseHandler = None
        switchType = type(switchValue)
        
        try:
            # Can we find an exact match for this switch value?
            # For an exact match, we will pass the case value to the case
            # handler.
            caseHandler = self.exactCases.get(switchValue)
            caseValue = switchValue
        except TypeError:
            pass

        # If no exact match, and we have 'in' cases to try,
        # see if we have a matching 'in' case for this switch value.
        # For an 'in' operation, we will be passing the left-hand side of
        # 'in' operator to the case handler.
        if not caseHandler and switchType in (STR_TYPE, LIST_TYPE, TUPLE_TYPE) \
           and self.inCases:
            caseValue, caseHandler = self._findInCase(switchValue)
        
        # If no 'in' match, and we have regex patterns to try,
        # see if we have a matching regex pattern for this switch value.
        # For a RegEx match, we will be passing the re.matchObject to the
        # case handler.
        if not caseHandler and switchType == STR_TYPE and self.patternCases:
            caseValue, caseHandler = self._findRegExCase(switchValue)
                    
        # If still no match, see if we have a default case handler to use.
        if not caseHandler:
            caseHandler = self.defaultHandler
            caseValue = switchValue
            
        # If still no case handler was found for the switch value, 
        # raise a SwitchError.
        if not caseHandler:        
            raise SwitchError("Unknown case value %r" % switchValue)
        
        # Call the case handler corresponding to the switch value,
        # passing it the case value, and any other parameters passed
        # to the switch, and return that case handler's return value.
        return caseHandler(caseValue, *args, **kwargs)
        
    ##
    # Register a case handler, and the case value is should handle.
    # This is a function decorator for a case handler.  It doesn't
    # actually modify the decorated case handler, it just registers it.
    # It takes a case value (any object that is valid as a dict key),
    # or any iterable of such case values.
    
    def case(self, caseValue):
        def wrap(caseHandler):
            
            # If caseValue is not an iterable, turn it into one so
            # we can handle everything the same.
            caseValues = ([ caseValue ] if not hasattr(caseValue, '__iter__') \
                          else caseValue)
                
            for aCaseValue in caseValues:
                # Raise SwitchError on a dup case value.
                if aCaseValue in self.exactCases:
                    raise SwitchError("Duplicate exact case value '%s'" % \
                                      aCaseValue)
                # Add it to the dict for finding exact case matches.
                self.exactCases[aCaseValue] = caseHandler
            
            return caseHandler
        return wrap
    
    ##
    # Register a case handler for handling a regular expression.
    def caseRegEx(self, caseValue):
        def wrap(caseHandler):
            
            # If caseValue is not an iterable, turn it into one so
            # we can handle everything the same.
            caseValues = ([ caseValue ] if not hasattr(caseValue, '__iter__') \
                          else caseValue)
                
            for aCaseValue in caseValues:
                # If this item is not a compiled regular expression, compile it.
                if type(aCaseValue) != CPAT_TYPE:
                    aCaseValue = re.compile(aCaseValue)
                    
                # Raise SwitchError on a dup case value.
                for thisCaseValue, _ in self.patternCases:
                    if aCaseValue.pattern == thisCaseValue.pattern:
                        raise SwitchError("Duplicate regex case value '%s'" % \
                                          aCaseValue.pattern)
                self.patternCases.append((aCaseValue, caseHandler))
                
            return caseHandler
        return wrap
        
    ##
    # Register a case handler for handling an 'in' operation.
    def caseIn(self, caseValue):
        def wrap(caseHandler):
            
            # If caseValue is not an iterable, turn it into one so
            # we can handle everything the same.
            caseValues = ([ caseValue ] if not hasattr(caseValue, '__iter__') \
                          else caseValue)
                
            for aCaseValue in caseValues:
                # Raise SwitchError on a dup case value.
                for thisCaseValue, _ in self.inCases:
                    if aCaseValue == thisCaseValue:
                        raise SwitchError("Duplicate 'in' case value '%s'" % \
                                          aCaseValue)
                # Add it to the the list of 'in' values.
                self.inCases.append((aCaseValue, caseHandler))
            
            return caseHandler
        return wrap
    
    ##
    # This is a function decorator for registering the default case handler.
    
    def default(self, caseHandler):
        self.defaultHandler = caseHandler
        return caseHandler

    
if __name__ == '__main__': # pragma: no cover
    
    # Example uses
    
    # Instantiate a switch object.
    mySwitch = Switch()
    
    # Register some cases and case handlers, using the handy-dandy
    # decorators.
    
    # A default handler
    @mySwitch.default
    def gotDefault(value, *args, **kwargs):
        print "Default handler: I got unregistered value %r, "\
              "with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value
        
    # A single numeric case value.
    @mySwitch.case(0)
    def gotZero(value, *args, **kwargs):
        print "gotZero: I got a %d, with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value

    # A range of numeric case values.
    @mySwitch.case(range(5, 10))
    def gotFiveThruNine(value, *args, **kwargs):    
        print "gotFiveThruNine: I got a %d, with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value
        
    # A string case value, for an exact match.
    @mySwitch.case('Guido')
    def gotGuido(value, *args, **kwargs):
        print "gotGuido: I got '%s', with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value
        
    # A string value for use with the 'in' operator.
    @mySwitch.caseIn('lo')
    def gotLo(value, *args, **kwargs):
        print "gotLo: I got '%s', with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value
        
    # A regular expression pattern match in a string.
    # You can also pass in a pre-compiled regular expression.
    @mySwitch.caseRegEx(r'\b([Pp]y\w*)\b')
    def gotPyword(matchObj, *args, **kwargs):
        print "gotPyword: I got a matchObject where group(1) is '%s', "\
              "with args: %r and kwargs: %r" % \
              (matchObj.group(1), args, kwargs)
        return matchObj
        
    # And lastly, you can pass a iterable to case, caseIn, and
    # caseRegEx.
    @mySwitch.case([ 99, 'yo', 200 ])
    def gotStuffInSeq(value, *args, **kwargs):
        print "gotStuffInSeq: I got %r, with args: %r and kwargs: %r" % \
              (value, args, kwargs)
        return value
    
    
    # Now show what we can do.
    got = mySwitch.switch(0)
    # Returns 0, prints "gotZero: I got a 0, with args: () and kwargs: {}"
    got = mySwitch.switch(6, flag='boring')    
    # Returns 6, prints "gotFiveThruNine: I got a 6, with args: () and
    # kwargs: {'flag': 'boring'}"
    got = mySwitch.switch(10, 42)
    # Returns 10, prints "Default handler: I got unregistered value 10,
    # with args: (42,) and kwargs: {}"
    got = mySwitch.switch('Guido', BDFL=True)
    # Returns 'Guido', prints "gotGuido: I got 'Guido', with args: () and 
    # kwargs: {'BDFL': True}"
    got = mySwitch.switch('Anyone seen Guido around?')
    # Returns 'Anyone Seen Guido around?', prints "Default handler: I got 
    # unregistered value 'Anyone seen Guido around?', with args: () and 
    # kwargs: {}", 'cause we used 'case' and not 'caseIn'.
    got = mySwitch.switch('Yep, and he said "hello".', 99, yes='no')
    # Returns 'lo', prints "gotLo: I got 'lo', with args: (99,) and 
    # kwargs: {'yes': 'no'}", 'cause we found the 'lo' in 'hello'.
    got = mySwitch.switch('Bird is the Python word of the day.')    
    # Returns a matchObject, prints "gotPyword: I got a matchObject where 
    # group(1) is 'Python', with args: () and kwargs: {}"
    got = mySwitch.switch('yo')
    # Returns 'yo', prints "gotStuffInSeq: I got 'yo', with args: () and
    # kwargs: {}"
