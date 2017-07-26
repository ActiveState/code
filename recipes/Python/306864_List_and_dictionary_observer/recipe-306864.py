"""
Implement an observer pattern for lists and dictionaries.

A subclasses for dicts and lists are defined which send information
about changes to an observer.

The observer is sent enough information about the change so that the
observer can undo the change, if desired.
"""
class list_observer(list):
    """
    Send all changes to an observer.
    """
    
    def __init__ (self,value,observer):
        list.__init__(self,value)
        self.set_observer(observer)
    
    def set_observer (self,observer):
        """
        All changes to this list will trigger calls to observer methods.
        """
        self.observer = observer 
    
    def __setitem__ (self,key,value):
        """
        Intercept the l[key]=value operations.
        Also covers slice assignment.
        """
        try:
            oldvalue = self.__getitem__(key)
        except KeyError:
            list.__setitem__(self, key, value)
            self.observer.list_create(self, key)
        else:
            list.__setitem__(self, key, value)
            self.observer.list_set(self, key, oldvalue)
    
    def __delitem__ (self,key):
        oldvalue = list.__getitem__(self, key)
        list.__delitem__(self, key)
        self.observer.list_del(self, key, oldvalue)
    
    def __setslice__ (self, i, j, sequence):
        oldvalue = list.__getslice__(self, i, j)
        self.observer.list_setslice(self, i, j, sequence, oldvalue)
        list.__setslice__(self, i, j, sequence)
    
    def __delslice__ (self, i, j):
        oldvalue = list.__getitem__(self, slice(i, j))
        list.__delslice__(self, i, j)
        self.observer.list_delslice(self, i, oldvalue)
    
    def append (self,value):
        list.append(self,value)
        self.observer.list_append(self)
    
    def pop (self):
        oldvalue = list.pop(self)
        self.observer.list_pop(self,oldvalue)
    
    def extend (self, newvalue):
        list.extend(self, newvalue)
        self.observer.list_extend(self, newvalue)
    
    def insert (self, i, element):
        list.insert(self, i, element)
        self.observer.list_insert(self, i, element)
    
    def remove (self, element):
        index = list.index(self, element)
        list.remove(self, element)
        self.observer.list_remove(self, index, element)
    
    def reverse (self):
        list.reverse(self)
        self.observer.list_reverse(self)
    
    def sort (self,cmpfunc=None):
        oldlist = self[:]
        list.sort(self,cmpfunc)
        self.observer.list_sort(self, oldlist)
        
class dict_observer(dict):
    """
    Send all changes to an observer.
    """
    def __init__ (self,value,observer):
        dict.__init__(self,value)
        self.set_observer(observer)
    
    def set_observer (self,observer):
        """
        All changes to this dictionary will trigger calls to observer methods
        """
        self.observer = observer 
    
    def __setitem__ (self,key,value):
        """
        Intercept the l[key]=value operations.
        Also covers slice assignment.
        """
        try:
            oldvalue = self.__getitem__(key)
        except KeyError:
            dict.__setitem__(self, key, value)
            self.observer.dict_create(self, key)
        else:
            dict.__setitem__(self, key, value)
            self.observer.dict_set(self, key, oldvalue)
    
    def __delitem__ (self, key):
        oldvalue = dict.__getitem__(self, key)
        dict.__delitem__(self, key)
        self.observer.dict_del(self, key, oldvalue)
    
    def clear (self):
        oldvalue = self.copy()
        dict.clear(self)
        self.observer.dict_clear(self, oldvalue)
    
    def update (self, update_dict):
        replaced_key_values =[]
        new_keys =[]
        for key, item in update_dict.items():
            if key in self:
                replaced_key_values.append((key,item))
            else:
                new_keys.append(key)
        dict.update(self, update_dict)
        self.observer.dict_update(self, new_keys, replaced_key_values)
    
    def setdefault (self, key, value=None):
        if key not in self:
            dict.setdefault(self, key, value)
            self.observer.dict_setdefault(self, key, value)
            return value
        else:
            return self[key]
    
    def pop (self, k, x=None):
        if k in self:
            value = self[k]
            dict.pop(self, k, x)
            self.observer.dict_pop(self, k, value)
            return value
        else:
            return x
    
    def popitem (self):
        key, value = dict.popitem(self)
        self.observer.dict_popitem(self,key,value)
        return key, value 

class printargs(object):
    """
    If a call to a method is made, this class prints the name of the method
    and all arguments.
    """
    def p(self, *args):
        print self.attr, args
    def __getattr__(self, attr):
        self.attr = attr
        return self.p

if __name__ == '__main__':
    # minimal demonstration of the observer pattern.
    observer = printargs()
    d = dict_observer({1:"one", 2:"two"}, observer)
    l = list_observer([1, 2, 3], observer)
    l.append(1)
    d[3]="Hello"
    d[53]="user"
    del d[1]
