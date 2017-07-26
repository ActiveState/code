'''
    JournalledDict

Implements the dictionary interface (with the help of DictMixin).
In this implementation, changes are not immediately stored, but instead
tracked in a journal.  When the value of a key is requested,
the journal is checked first and provides the most recent value.

The method apply() replays the journal to update the
underlying dictionary, and wipe() throws away all
recent changes without saving.  Both clear the journal.

I designed this class to implement transaction-like behavor
on local objects; you can add that behavor to a class with the
JournalledMixin.

JournalledDict only implements the minimal set of special
methods needed for DictMixin to provide the full interface.
So, methods like iteritems() will not give good performance.

Note that mutating the values of attributes is not (and cannot)
be journalled.
'''

import UserDict

class Change(object):
    ' A single set or del. The journal is a list of Changes. '
    def __init__(self, action, key, value):
        self.action = action
        self.key = key
        self.value = value
    def __repr__(self):
        return '<%s%s:%s>' % (self.action, self.key,self.value)

class JournalledDict(UserDict.DictMixin):
    'A dictionary with journalling behavor.'
    def __init__(self,prototype=None,**kwargs):
        self.base = prototype if prototype else {}
        self.base.update(kwargs)
        self.changes = []

    def __setitem__(self,key,value):
       # add to the front of the journal
        self.changes[0:0] = [ Change('+',key,value) ]

    def __delitem__(self,key):
        self[key]  # correctly raises KeyError if the key isn't defined
        self.changes[0:0] = [ Change('-',key,None) ]

    def __getitem__(self, key):
        for change in self.changes:
            if change.key == key:
                if change.action == '+':
                    return change.value
                elif change.action == '-':
                    raise KeyError,key
        return self.base[key]

    def apply(self):
        'play the journal back onto the base dictionary.'
        for change in self.changes:
            if change.action == '+':
                self.base[change.key] = change.value
            elif change.action == '-':
                del self.base[change.key]
        self.wipe()
        
    def wipe(self):
        'clear the journal, reverting to the last applied state.'
        self.changes = []

    def keys(self):
        'provide an iterable of keys.'
        keys = set(self.base.keys())
        for change in self.changes:
            if change.action == '+':
                keys.add(change.key)
            elif change.action == '-':
                keys.remove(change.key)
        return keys

class JournalledMixin(object):
    'Gives an class journaling behavor.'
    'JournalledMixin should be listed FIRST in the list of base classes.'
    
    def __init__(self, *args, **kwargs):
        self.__dict__['_journal'] = JournalledDict(self.__dict__)
        super(JournalledMixin, self).__init__(*args, **kwargs)
        # Save the state after giving other bases classes a chance to initialize.
        JournalledMixin.applyJournal(self)
        
    def __getattr__(self, name): return self.__dict__['_journal'][name]
    def __setattr__(self, name, value): self.__dict__['_journal'][name] = value
    def __delattr__(self, name): del self.__dict__['_journal'][name]
    
    def wipeJournal(self):
        'clear the journal and throw away all recent changes.'
        self.__dict__['_journal'].wipe()
        
    def applyJournal(self):
        'Save all recent changes and start a new journal.'
        self.__dict__['_journal'].apply()

### Test Cases ###
        
if __name__ == '__main__':
    class Position(object):
        'A trivial class used to test the Mixin.'
        def __init__(self,x=0,y=0):
            self.x = x
            self.y = y
        def __str__(self):
            return '(%s, %s)' % (self.x, self.y)

    class JournalledPosition(JournalledMixin, Position):
        'A trivial class with journalling behavor.'
        pass

    print 'Basic Example:'
    print '--------------'
    print 'start with a small Journalled Dictionary:'
    jd = JournalledDict(x=1,y=2)
    print jd.base
    print jd.changes
    jd['x'] = 4
    jd['z'] = 7
    del jd['y']
    print 'making a couple changes:'
    print jd.base
    print jd.changes
    print 'now we apply the journal:'
    jd.apply()
    print jd.base
    print jd.changes
    print 'make a couple more changes:'
    del jd['x']
    jd['y'] = 15
    print jd.base
    print jd.changes
    print 'and wipe the journal:'
    jd.wipe()
    print jd.base
    print jd.changes
    print
    print
    print 'Mixin Example:'
    print '--------------'
    jp = JournalledPosition(1,2)
    print 'a fresh JournalledPosition instance:'
    print jp
    print 'we update the attributes:'
    jp.x = 7
    jp.y = -4
    print jp
    print 'but it goes right back after we call wipeJournal():'
    jp.wipeJournal()
    print jp
    print 'we change x and call applyJournal():'
    jp.x = 11
    jp.applyJournal()
    print jp
    print 'now calling wipeJournal() does nothing:'
    jp.wipeJournal()
    print jp
