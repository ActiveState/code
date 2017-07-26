"""
Implement an observer pattern for attribute access.

Assumes that each attribute is used (exclusivly) for either scalar
values, lists or maps.

It does not work if you store a scalar in an attribute, and then later
a map or list.

A scalar attribute is an attribute whose values do not have internal
structure.  Scalars are integers, floats, (short) strings, and
references to instances and classes.

Provides some support to observe lists and dictionaries which are
assigned to attributes.

Usage pattern:
    class c(object):
        ...some definitions...
    
    class observer_class(object):
        ...some definitions...
        
    observer = observer_class()
        
    c.x = scalar_observer("x", observer)
    i = c()
    i.x = 13
    # The assignment above will trigger a method call to observer.
    
    For lists, you can use:
        
    c.l = list_observer_in_instance("l", observer)
    i = c()
    i.l = l = [1, [1, 2], 3]
    i.l.append(4)
    # The append above will trigger a method call to observer.
    # Two caveats here:
    #     1. i.l now points to a different list than l.
    #        (you should probably avoid such aliasing).
    #        If you want to continue to use l, you should
    #        probably add:
    #        l = i.l
    #     2. The inner list [1, 2] is *not* monitored.
    #        (if desired, invoke list_observer([1, 2], observer) instead
    #         of just [1, 2]).
    
The attribute is replaced by a descriptor in the class. The attributes
in the instances have too leading underscores (__).
"""

from list_dict_observer import list_observer, dict_observer, printargs
    
class scalar_observer(object):
    """
    Observes a scalar attribute.
    
    Can be used for integers, longs, floats, (short) strings, and
    references to instances or classes.
    
    Lists and dictionaries have specialized classes.
    
    All assignments to the attributes are intercepted by
    descriptors. The values themselves are stored in an attribute with
    a name __<attributename>.
    """
    def __init__ (self, external_attributename, observer):
        self.external_attributename = external_attributename 
        self.private_attributename = '__'+external_attributename 
        self.observer = observer 
    
    def __set__ (self, instance, value):
        private_attributename = self.private_attributename 
        external_attributename = self.external_attributename 
        try:
            oldvalue = getattr(instance, private_attributename)
        except AttributeError:
            setattr(instance, private_attributename, value)
            self.observer.scalar_set(instance, private_attributename, external_attributename)
        else:
            if oldvalue!=value:
                setattr(instance, private_attributename, value)
                self.observer.scalar_modify(instance, private_attributename, external_attributename, oldvalue)
    def __get__ (self, instance, owner):
        return getattr(instance, self.private_attributename)
    
class list_observer_in_instance(object):
    """
    Observes instance attributes which contain a list as a value.
    
    Assignments to these attributes, which must be lists, are replaced by instances of 'list_observer'.
    
    Note that you are not notified by changes to inner lists or maps.
    
    You should also be aware of aliasing.
    """
    
    def __init__ (self, external_attributename, observer):
        self.external_attributename = external_attributename 
        self.internal_attributename = '__'+external_attributename 
        self.observer = observer 
    
    def __set__ (self, instance, value):
        """Intercept assignments to the external attribute"""
        assert isinstance(value, type([]))
        if isinstance(value, list_observer):
            newvalue = value 
            # if the value is already a list observer, assume that this value
            # already has an observer. Do new create a new list in this case.
        else:
            newvalue = list_observer(value, self.observer)
        internal_attributename = self.internal_attributename 
        try:
            oldvalue = getattr(instance, internal_attributename)
        except AttributeError:
            self.observer.list_assignment_new(instance, internal_attributename)
        else:
            self.observer.list_assignment_replace(instance, internal_attributename, oldvalue)
        setattr(instance, self.internal_attributename, newvalue)
    
    def __get__ (self,instance,owner):
        try:
            return instance.__dict__[self.internal_attributename]
        except KeyError:
            return instance.__dict__[self.external_attributename]
    
class dict_observer_in_instance(object):
    """
    observes instance attributes which contain a list as a value.
    
    Assignments to this attributes, which must be dictionaries, are
    replaced by instances of 'dict_observer'.

    Note that you are not notified by changes to inner lists or maps.
    
    You should also be aware of aliasing.
    """
    def __init__ (self, external_attributename, observer):
        self.external_attributename = external_attributename 
        self.internal_attributename = '__'+external_attributename 
        self.observer = observer 
    
    def __set__ (self, instance, value):
        """Intercept assignments to the external attribute"""
        assert isinstance(value,type({}))
        if isinstance(value,dict_observer):
            newvalue = value 
            # if the value is already a dict_observer,
            # assume that the value is already monitored.
        else:
            newvalue = dict_observer(value, self.observer)
            internal_attributename = self.internal_attributename 
            try:
                oldvalue = getattr(instance, internal_attributename)
            except AttributeError:
                setattr(instance, self.internal_attributename, newvalue)
                self.observer.list_assignment_new(instance, internal_attributename)
            else:
                setattr(instance, self.internal_attributename, newvalue)
                self.observer.list_assignment_replace(instance, internal_attributename, oldvalue)
    
    def __get__ (self, instance, owner):
        try:
            return instance.__dict__[self.internal_attributename]
        except KeyError:
            return instance.__dict__[self.external_attributename]
    
if __name__ == '__main__':
    # minimal demonstration of the observer pattern.
    class c(object):
        pass
    observer = printargs()
    i = c()
    c.s = scalar_observer("x", observer)
    i.s = 1
    i.s = "hello"
    c.l = list_observer_in_instance("l", observer)
    i.l = [1, 2, 3]
    i.l.append(1)
