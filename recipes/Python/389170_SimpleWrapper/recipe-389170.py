"""
SimpleWrapper 1.0
Author: Jonas Galvez <jonasgalvez@gmail.com>
"""

class SimpleWrapper:
    class MethodCall:
        def __init__(self, function, *params):
            self.function = function
            self.default_params = params
        def __call__(self, *params):
            return self.function(*(self.default_params + params))
    def __init__(self, ns, *params):
        self.params = params
        self.ns =  ns
    def __getattr__(self, attr):
        return SimpleWrapper.MethodCall(self.ns[attr], *self.params);

if __name__ == '__main__':

    # Simple esage example
    # ---------------------------------------------------
    def foo(a, b,  c):
        print a, b, c

    def bar(a, b, c):
        print a, b, c

    o = SimpleWrapper(globals(), 1)
    o.foo(2, 3)
    o.bar(4, 5)
    # ---------------------------------------------------

    # And here's the scenario that led me into coding it:
    # ---------------------------------------------------

    def main(u, p, *db_data):
        db = connect_db('localhost', *db_data)
        db.create_table()
        db.populate_table(feeds)

    # ...

    def connect_db(*k):
        import MySQLdb
        conn = MySQLdb.connect(*k)
        return SimpleWrapper(globals(), conn.cursor())

    def create_table(cursor):
        pass # ...

    def populate_table(cursor, feeds):
        pass # ...

    # ---------------------------------------------------
