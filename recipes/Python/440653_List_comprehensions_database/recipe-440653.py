"""A wrapper around DBAPI-compliant databases to support iteration
and list comprehension syntax for requests, instead of SQL

To get an iterator, initialize a connection to the database, then

tbl = Table(connection,table_name)

returns an iterator that yields records (instances of the generic
class Record) whose attributes match the fields in the database

You can also choose to return a dictionary or a list with the
method set_return_type()

Example of use with sqlite :

    from pysqlite2 import dbapi2 as sqlite

    conn = sqlite.connect('planes')
    plane_tbl = Table(conn,'plane')
    country_tbl = Table(conn,'countries')

    # simple requests
    print [ r.name for r in plane_tbl if r.country == 'France' ]
    print [ r.country for r in country_tbl if r.continent == 'Europe']

    # request on two tables
    print [r.name for r in plane_tbl for c in country_tbl 
            if r.country == c.country and c.continent == 'Europe']

"""

class Record(object):
    """A generic class for database records"""
    pass

class Table:

    def __init__(self,conn,table):
        self.table = table
        self.cursor = conn.cursor()
        self._iterating = False
        # to initialize cursor.description, make a select request
        self.sql = "SELECT * FROM %s" %self.table
        self.cursor.execute(self.sql)
        self.names = [ d[0] for d in self.cursor.description ]
        self.return_type = object
    
    def set_return_type(self,rt):
        if not rt in [object,list,dict]:
            raise TypeError,"Invalid return type %s" %rt
        else:
            self.return_type = rt
        
    def __iter__(self):
        return self
    
    def next(self):
        if not self._iterating:
            # begin iteration
            self.cursor.execute(self.sql)
            self._iterating = True
        row = self.cursor.fetchone()
        if row is not None:
            if self.return_type == object:
                # transform list into instance of Record
                rec = Record()
                rec.__dict__ = dict(zip(self.names,row))
                return rec
            elif self.return_type == dict:
                return dict(zip(self.names,row))
            elif self.return_type == list:
                return row
        self._iterating = False
        raise StopIteration
