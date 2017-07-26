# ordereddict.py
# A dictionary that remembers insertion order
# Tested under Python 2.7 and 2.6.6 only
#
# Copyright (C) 2011 by Lucio Santi <lukius at gmail dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from _abcoll import *
try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident
    
from operator import eq as _eq
from itertools import imap as _imap

__author__ = 'Lucio Santi <lukius at gmail dot com>'
__version__ = '1.1'
__all__ = ['OrderedDict']



########################### Constants ###########################
FORWARD = 0
BACKWARDS = 1

KEY = 0
VALUE = 1
NEXT = 3
PREVIOUS = 2
#################################################################


class OrderedDict(dict, MutableMapping):
    'A dictionary that remembers insertion order.'
  
    # This implementation uses a doubly-linked list of nodes, each
    # node being a 4-tuple <key, value, previous node, next node>.
    # Despite this, the interesting thing about it is that the list
    # is actually embedded in the dictionary. As a consequence,
    # there is little space penalty, and also every operation
    # exhibits an efficient implementation (i.e., no need to perform 
    # lookups or deletions multiple times, as it happens with other 
    # versions of this data structure.).
    #
    # It is worth noticing that passing an OrderedDict as an argument
    # to the dict constructor won't behave as expected. This is due
    # to the fact that the internal dictionary keeps additional information
    # apart from a key's value. If needed, the instance method dict()
    # provides a dict copy of an OrderedDict.
  
    update = MutableMapping.update
    setdefault = MutableMapping.setdefault
    __ne__ = MutableMapping.__ne__

    ######################## Class methods #########################
    @classmethod
    def fromkeys(cls, iterable, value = None):
        '''od.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        '''      
        d = cls()
        for key in iterable:
            d[key] = value
        return d
    ################################################################    


    ######################## Initialization ########################
    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.
        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.first_node
        except AttributeError:    
            self.first_node = None
            self.last_node = None
	self.update(*args, **kwds)
    ################################################################
     
     
    ################## Data access & manipulation ##################
    __marker = object()
    
    def __getitem__(self, key):
        'od.__getitem__(y) <==> od[y]'
        node = dict.__getitem__(self, key)
        return node[VALUE]
        
    def get(self, key, default = None):
        'od.get(k[,d]) -> od[k] if k in od, else d.  d defaults to None.'
        try:
            value = self.__getitem__(key)
        except KeyError:
            value = default
        return value          
        
    def __setitem__(self, key, value):
        'od.__setitem__(i, y) <==> od[i]=y'
        try:
            node = dict.__getitem__(self, key)
            node[VALUE] = value
        except KeyError:
            new_node =  [key, value, self.last_node, None]
            if( self.first_node is None ):
              self.first_node = new_node
            if( self.last_node is not None ):
              self.last_node[NEXT] = new_node
            self.last_node = new_node
            dict.__setitem__(self, key, new_node)

    def __delitem__(self, key):
        'od.__delitem__(y) <==> del od[y]'
        removed_node = dict.pop(self,key)
        self.__adjust_after_removing(removed_node)

    def pop(self, key, default = __marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value. If key is not found, d is returned if given, otherwise KeyError
        is raised.'''
        removed_node = dict.pop(self, key, default)
        if( removed_node is self.__marker ):
            raise KeyError, key
        if( removed_node is default ):
            return default
        self.__adjust_after_removing(removed_node)
        return removed_node[VALUE]
        
    def popitem(self, last = True):
        '''od.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if od is empty.'''
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return key, value
        
    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        dict.clear(self)
        self.first_node = None
        self.last_node = None        
        
    def __adjust_after_removing(self, a_node):
        'Adjust a_node previous and next pointers after its removal.'
        previous = a_node[PREVIOUS]
        next = a_node[NEXT]
        
        if( next ):
            next[PREVIOUS] = previous
        else:
            self.last_node = previous        
        if( previous ):
            previous[NEXT] = next
        else:
            self.first_node = next
    ################################################################        
     
     
    #################### Iteration & keys/values ################### 
    def __walk(self, direction = FORWARD, action = lambda x: x, *arguments):
        'Iterate over action applied to each node, in the appropriate order.'
        if( direction == FORWARD ):
            next = NEXT
            first = self.first_node
        elif( direction == BACKWARDS ):
            next = PREVIOUS
            first = self.last_node
        current_node = first
        while( current_node ):
            yield action(current_node, *arguments)
            current_node = current_node[next]        
            
    def __walk_to_list(self, direction = FORWARD, action = lambda x: x, *arguments):
        '''Obtain a list of objects resulting from applying action to
        each node, in the appropriate order.'''
        return_list = list()
        item_generator = self.__walk(direction = direction, action = action, *arguments)
        for item in item_generator: return_list.append(item)
        return return_list
      
    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        return self.__walk( action = lambda node: node[KEY] )
            
    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        return self.__walk( direction = BACKWARDS, action = lambda node: node[KEY] )   
               
    def keys(self):
        "od.keys() -> list of od's keys"
        return self.__walk_to_list( action = lambda node: node[KEY] )      

    def values(self):
        "od.values() -> list of od's values"
        return self.__walk_to_list( action = lambda node: node[VALUE] )
  
    def items(self):
        "od.items() -> list of od's (key, value) pairs, as 2-tuples"
        return self.__walk_to_list( action = lambda node: (node[KEY], node[VALUE]) )
        
    def iterkeys(self):
        'od.iterkeys() -> an iterator over the keys of od'
        return iter(self)
        
    def itervalues(self):
        'od.itervalues() -> an iterator over the values of od'
        return self.__walk( action = lambda node: node[VALUE] )

    def iteritems(self):
        'od.iteritems() -> an iterator over the (key, value) items of od'
        return self.__walk( action = lambda node: (node[KEY], node[VALUE]) )
    ################################################################    
        
        
    ############################# Copies ###########################
    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)    

    def dict(self):
        'od.dict() -> a dict copy of od'
        d = {}
        for item in self.iteritems(): d[item[KEY]] = item[VALUE]
        return d
    ################################################################        
    
    
    ########################## Miscellaneous #######################
    def __repr__(self, _repr_running = {}):
        'od.__repr__() <==> repr(od)'
        call_key = id(self), _get_ident()
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]
            
    def __reduce__(self):
        'Return state information for pickling'
        items = self.items()
        tmp = self.first_node, self.last_node
        del self.first_node, self.last_node
        inst_dict = vars(self).copy()
        self.first_node, self.last_node = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''      
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and \
                   all(_imap(_eq, self.iteritems(), other.iteritems()))
        return dict.__eq__(self.dict(), other)
        
    def viewkeys(self):
        "od.viewkeys() -> a set-like object providing a view on od's keys"
        return KeysView(self)

    def viewvalues(self):
        "od.viewvalues() -> an object providing a view on od's values"
        return ValuesView(self)

    def viewitems(self):
        "od.viewitems() -> a set-like object providing a view on od's items"
        return ItemsView(self)
    ################################################################
