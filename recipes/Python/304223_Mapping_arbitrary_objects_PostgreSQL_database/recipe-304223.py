from datetime import datetime
 
import psycopg
from psycopg.extensions import adapters, adapt

try: sorted()
except NameError:
    def sorted(seq):
        seq.sort()
        return seq

# Here is the adapter for every object that we may ever need to 
# insert in the database. It receives the original object and does
# its job on that instance
class ObjectMapper(object):
    def __init__(self, orig):
        self.orig = orig
        self.tmp = {}
        self.items, self.fields = self._gatherState()
 
    def _gatherState(self):
        adaptee_name = self.orig.__class__.__name__
        fields = sorted([(field, getattr(self.orig, field))
                        for field in persistent_fields[adaptee_name]])
        items = []
        for item, value in fields:
            items.append(item)
        return items, fields
 
    def getTableName(self):
        return self.orig.__class__.__name__
 
    def getMappedValues(self):
        tmp = []
        for i in self.items:
            tmp.append("%%(%s)s"%i)
        return ", ".join(tmp)
 
    def getValuesDict(self):
        return dict(self.fields)
 
    def getFields(self):
        return self.items

    def generateInsert(self):
        qry = "INSERT INTO"
        qry += " " + self.getTableName() + " ("
        qry += ", ".join(self.getFields()) + ") VALUES ("
        qry += self.getMappedValues() + ")"
        return qry, self.getValuesDict()

# Here are the objects
class Album(object):    
    id = 0 
    def __init__(self):
        self.creation_time = datetime.now()
        self.album_id = self.id
        Album.id = Album.id + 1
        self.binary_data = buffer('12312312312121')
 
class Order(object):
     id = 0
     def __init__(self):
        self.items = ['rice','chocolate']
        self.price = 34
        self.order_id = self.id
        Order.id = Order.id + 1
 
adapters.update({Album: ObjectMapper, Order: ObjectMapper})
    
# Describe what is needed to save on each object
# This is actually just configuration, you can use xml with a parser if you
# like to have plenty of wasted CPU cycles ;P.
persistent_fields = {'Album': ['album_id', 'creation_time', 'binary_data'],
                     'Order': ['order_id', 'items', 'price']
                    }
 
print adapt(Album()).generateInsert()
print adapt(Album()).generateInsert()
print adapt(Album()).generateInsert()
print adapt(Order()).generateInsert()
print adapt(Order()).generateInsert()
print adapt(Order()).generateInsert()
