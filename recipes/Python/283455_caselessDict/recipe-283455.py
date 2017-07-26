#  27-05-04
# v2.0.2
#

# caseless
# Featuring :

# caselessDict
# A case insensitive dictionary that only permits strings as keys.

# Implemented for ConfigObj
# Requires Python 2.2 or above

# Copyright Michael Foord
# Not for use in commercial projects without permission. (Although permission will probably be given).
# If you use in a non-commercial project then please credit me and include a link back.
# If you release the project non-commercially then let me know (and include this message with my code !)

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail fuzzyman AT atlantibots DOT org DOT uk (or michael AT foord DOT me DOT uk )
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html


class caselessDict(dict):
    """A case insensitive dictionary that only permits strings as keys."""
    def __init__(self, indict={}):
        dict.__init__(self)
        self._keydict = {}                      # not self.__keydict because I want it to be easily accessible by subclasses
        for entry in indict:
            self[entry] = indict[entry]         # not dict.__setitem__(self, entry, indict[entry]) becasue this causes errors (phantom entries) where indict has overlapping keys... 

    def findkey(self, item):
        """A caseless way of checking if a key exists or not.
        It returns None or the correct key."""
        if not isinstance(item, str): raise TypeError('Keywords for this object must be strings. You supplied %s' % type(item))
        key = item.lower()
        try:
            return self._keydict[key]
        except:
            return None
    
    def changekey(self, item):
        """For changing the casing of a key.
        If a key exists that is a caseless match for 'item' it will be changed to 'item'.
        This is useful when initially setting up default keys - but later might want to preserve an alternative casing.
        (e.g. if later read from a config file - and you might want to write back out with the user's casing preserved).
        """
        key = self.findkey(item)           # does the key exist
        if key == None: raise KeyError(item)
        temp = self[key]
        del self[key]
        self[item] = temp
        self._keydict[item.lower()] = item
            
    def lowerkeys(self):
        """Returns a lowercase list of all member keywords."""
        return self._keydict.keys()

    def __setitem__(self, item, value):             # setting a keyword
        """To implement lowercase keys."""
        key = self.findkey(item)           # if the key already exists
        if key != None:
            dict.__delitem__(self,key)
        self._keydict[item.lower()] = item
        dict.__setitem__(self, item, value)

    def __getitem__(self, item):
        """To implement lowercase keys."""
        key = self.findkey(item)           # does the key exist
        if key == None: raise KeyError(item)
        return dict.__getitem__(self, key) 

    def __delitem__(self, item):                # deleting a keyword
        key = self.findkey(item)           # does the key exist
        if key == None: raise KeyError(item)
        dict.__delitem__(self, key)
        del self._keydict[item.lower()]

    def pop(self, item, default=None):
        """Correctly emulates the pop method."""
        key = self.findkey(item)           # does the key exist
        if key == None:
            if default == None:
                raise KeyError(item)
            else:
                return default
        del self._keydict[item.lower()]
        return dict.pop(self, key)
    
    def popitem(self):
        """Correctly emulates the popitem method."""
        popped = dict.popitem(self)
        del self._keydict[popped[0].lower()]
        return popped
    
    def has_key(self, item):
        """A case insensitive test for keys."""
        if not isinstance(item, str): return False               # should never have a non-string key
        return self._keydict.has_key(item.lower())           # does the key exist
        
    def __contains__(self, item):
        """A case insensitive __contains__."""
        if not isinstance(item, str): return False               # should never have a non-string key
        return self._keydict.has_key(item.lower())           # does the key exist

    def setdefault(self, item, default=None):
        """A case insensitive setdefault.
        If no default is supplied it sets the item to None"""
        key = self.findkey(item)           # does the key exist
        if key != None: return self[key]
        self.__setitem__(item, default)
        self._keydict[item.lower()] = item
        return default
    
    def get(self, item, default=None):
        """A case insensitive get."""
        key = self.findkey(item)           # does the key exist
        if key != None: return self[key]
        return default

    def update(self, indict):
        """A case insensitive update.
        If your dictionary has overlapping keys (e.g. 'FISH' and 'fish') then one will overwrite the other.
        The one that is kept is arbitrary."""
        for entry in indict:
            self[entry] = indict[entry]         # this uses the new __setitem__ method            

    def copy(self):
        """Create a new caselessDict object that is a copy of this one."""
        return caselessDict(self)

    def dict(self):
        """Create a dictionary version of this caselessDict."""
        return dict.copy(self)
    
    def clear(self):
        """Clear this caselessDict."""
        self._keydict = {}
        dict.clear(self)

    def __repr__(self):
        """A caselessDict version of __repr__ """
        return 'caselessDict(' + dict.__repr__(self) + ')'
    
    

    
##############################################################



# brief test stuff
if __name__ == '__main__':
    print 'caselessDict Tests'
    b = { 'FISH' : 'fish' }
    a = caselessDict(b)
    print "An apparently standard dict."
    print a
    print "a['FisH'] = ", a['FisH']
    b = {1 : 'fail'}
    print "We will now check that creating a caselessDict with an integer key fails."
    try:
        print caselessDict(b)
        print "oops - that shouldn't have worked"
    except Exception, e:
        print 'Exception : '
        print e
        print 'Good'
    print 'Testing deleting a key'
    del a['Fish']
    print "del a['Fish']\na = ", a
    a['FISH'] = 'fish'
    print 'Reset a[\'FISH\'] again and then pop the value : ', a.pop('fish')
    print 'Reset a[\'FISH\'] again and then test if it has the key : '
    a['FISH'] = 'fish'
    print 'a.has_key(\'fish\') : ', a.has_key('fish')
    print 'Let\'s test the __contains__ method by doing an if \'FiSH\' in a test :', 'FiSH' in a
    print 'setdefault, first with the keyword \'FISh\' and default of None. Then with keyword \'FROG\' and default None.'
    print a.setdefault('FISh', None)
    print a.setdefault('FROG', None)
    print a
    print 'Next get - but with keys \'FIsH\' and \'PIANO\' and default of False.'
    print a.get('FIsH', False)
    print a.get('PIANO', False)
    print 'An update - we\'ll add the key \'PIANO\'.'
    a.update({'PIANO' : ' A Piano'})
    print a
    print 'Popitem :', 
    print a.popitem()
    print a
    b = a.copy()
    b.clear()
    b['FISH'] = 'fish'
    print 'The following is a copy, then cleared (clear method), a new key added.'
    print 'We then test the type of the new dictionary...'
    print b
    print type(b)
    print 'The keys :'
    print b.keys()
    
        

"""
TODO
fromkeys returns a dict - not a caselessDict
The findkey method could be inline wherever it's used - to improve speed. (Use psyco instead - this inlines small functions !)
Could methods of caselessDict that return lists return caselessLists ? (e.g. keys)
Only allow strings or lists as values ? (This would be useful for me - but less useful for others)
If I knew how to implement iterators I could increase the speed further !!


ISSUES
If you initialise or update with a dictionary that has overlapping keys (e.g. 'FISH' and 'fish') then one entry will overwrite the other..
The one that is kept is arbitrary !



CHANGELOG

27-05-02       Version 2.0.2
Added the clear and __repr__ methods.

25-05-04       Version 2.0.1
Changed the findkey method to using a try/except test.. quicker for lookups.
*Slightly* optimised __init__ (removed duplicate type check)...

24-05-04       Version 2.0.0
Changed the way caselessDict work - it now uses an internal dict to keep track of keys
This should be *much* quicker (although still twice as slow as a standard dict !)
Added the popitems method - needed for new implementation.
Changed pop and setdefault to properly mimic dict, with the optional argument.
Added the dict method.


17-05-04       Version 1.1.1
Added the changekey method to caselessDict. Don't ask !! 

15-05-04       Version 1.1.0
Added caselessList a caseless List implementation.
Lot more work than dict actually - more methods to implement for a sequence object.
Changed module name from caselessDict to caseless.

13-05-04       Version 1.0.2
Added lowerkeys method.
Renamed _caselessfind method to 'findkey'

10-05-04       Version 1.0.1
Slight change to allow '' as a valid key.

09-05-04       Version 1.0.0
First version. Seems to work.
I don't understand __new__ but all the other keys seem to work.
popitem, keys, fromkeys etc seem to work without being explicitly defined.

"""
