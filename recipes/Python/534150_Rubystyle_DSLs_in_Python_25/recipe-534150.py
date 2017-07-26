from __future__ import with_statement
from contextlib import contextmanager

class Table(object):
    def __init__(self, table_name):
        self.table_name = table_name
        self.fields = {}

    def __setattr__(self, attr, value):
        if attr in ("fields", "table_name"):
            object.__setattr__(self, attr, value)
        else:
            self.fields[attr] = value

    def execute(self):
        print "Creating table %s with fields: %s" % (self.table_name, self.fields)

@contextmanager
def create_table(table_name):
    table=Table(table_name)
    yield table
    table.execute()

#try it!
with create_table("Employee") as t:
    t.first_name = {"type" : "char", "length" : 30 }
    t.last_name = {"type" : "char", "length" : 30 }
    t.age = {"type" : "int"}

#prints:
#Creating table Employee with fields: {'first_name': {'length':
#30, 'type': 'char'}, 'last_name': {'length': 30, 'type': 'char'}, 'age':
#{'type': 'int'}}
