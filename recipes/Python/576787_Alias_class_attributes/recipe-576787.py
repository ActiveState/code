"""
Alias allows the dynamic aliasing of class attributes to a sequence of aliases
using metaclass programming to give a declarative way of expressing aliases as
an inner class on the object in question.

The main use of such a system would be to unify a disparate set of objects with
similar, but differently named attributes so that they can access be a single
piece of code.

Taking the example below, we define two types of records - an old-style and
new-style record. Note that the attributes on the class describe the same
things, but are named differently. By declaring a set of suitable aliases on
each style class we can then include both styles in our record set and treat
them as one:

>>> from alias import NewRecord, OldRecord, RecordSet
>>> rs = RecordSet(NewRecord(), OldRecord())
>>> rs.records
[<alias.NewRecord object at ...>, <alias.OldRecord object at ...>]
>>> rs.sort_by_added()
>>> rs.records
[<alias.OldRecord object at ...>, <alias.NewRecord object at ...>]
>>> [r.removed for r in rs.records]
[False, False]
>>> rs.mark_all_as_removed()
>>> [r.removed for r in rs.records]
[True, True]
>>> [r.deleted for r in rs.records]
[True, True]
>>> for r in rs.records: r.save()
Storing record: Old type record
Saving record: New style record
"""
import inspect

class AliasDescriptor(object):
    def __init__(self, alias):
        self.alias = alias
    
    def __get__(self, instance, owner):
        return getattr(instance, owner.__dict__['__aliases'][self.alias])
    
    def __set__(self, instance, value):
        setattr(instance,
                instance.__class__.__dict__['__aliases'][self.alias],
                value)
    
    def __delete__(self, instance):
        raise AttributeError('Deleting of aliased attribute %r is not supported' % self.alias)
        

class AliasType(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(AliasType, cls).__new__(cls, name, bases, attrs)
        
        # see whether we've got an Alias inner class:
        if inspect.isclass(attrs.get('Alias', None)):
            alias = attrs['Alias']
            setattr(new_class, '__aliases', {})
            for attr, value in alias.__dict__.items():
                # don't want any "private" attrs appearing
                if attr.startswith('_'):
                    continue
                # don't care if these aren't tuples or lists
                if not isinstance(value, (tuple, list)):
                    continue
                # no point in setting up an alias for something which isn't a
                # class attribute:
                if not attr in attrs:
                    continue
                
                # if we've got to here put the lookups into the __aliases dict:
                for key in value:
                    new_class.__dict__['__aliases'][key] = attr
                    setattr(new_class, key, AliasDescriptor(key))
            
        return new_class

class Aliaser(object):
    __metaclass__ = AliasType
    
from datetime import datetime

class BaseRecord(object):
    """Dummy base class to demonstrate multiple-inheretance"""
    pass

class OldRecord(BaseRecord, Aliaser):
    title = 'Old type record'
    created = datetime(2007, 1, 1, 9)
    deleted = False
    
    def store(self):
        print 'Storing record: %s' % self.title
    
    class Alias:
        created = ('date_created', 'created_date', 'added')
        deleted = ('removed',)
        store = ('save',)
        
class NewRecord(BaseRecord, Aliaser):
    title = "New style record"
    added = datetime(2009, 1, 1, 10)
    removed = False
    
    def save(self):
        print 'Saving record: %s' % self.title
    
    class Alias:
        added = ('date_created', 'created_date', 'created')
        removed = ('deleted',)
        save = ('store')
        
class RecordSet(object):
    def __init__(self, *records):
        self.records = list(records)
    
    def sort_by_added(self):
        self.records.sort(key=lambda r: r.added)
    
    def mark_all_as_removed(self):
        for record in self.records:
            record.removed = True

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
