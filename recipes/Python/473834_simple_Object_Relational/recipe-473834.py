from Cheetah.Template import Template
import psycopg
conn = psycopg.connect(database="demo")
class Model:
    '''A class providing limited introspective access to (currently) 
    a Postresql Database.
    '''
    global conn 
    def __init__(self, connection=conn):
        self.conn = connection

    def __getattr__(self, name):
        """Returns a subclass of Relation for each table found in
        the model.

        N.B. This returns a class object rather than an instance.  From
        this object you can:-
           - query the database for a cursor,
           - instantiate an instance of the class (i.e. a single row 
             from the database)
           - obtain meta-data from the database table or view
        """
        if name.lower() in self.tables():
            DataSource = type(name, (Relation, dict), {})
            return DataSource
        else:
            raise AttributeError, 'Attribute %s not found' % name


    def getView(self, view_name):
        """The same as __getattr__ except from here, you're allowed to
        specify the view as a string (rather than an object)
        """
        if view_name.lower() in self.tables_and_views():
            DataSource = type(view_name, (Relation, type), {'conn': self.conn})
            return DataSource
        else:
            raise ValueError, 'View %s not found' % view_name


    def tables_and_views(self, schemas=None):
        """Returns a list of tables and views contained in the database on the
        current connection.

        If specified, schemas should be an iterable of schemas from which the
        tables/views should be gathered
        """
        sql = '''select tablename
                 from pg_tables
        	 union
        	 select viewname
        	 from pg_views
        '''
        if schemas:
            sql += "where schemaname in ("
            sql += ", ".join(["%s" for i in schemas]) + ")" 
        cursor = self.conn.cursor()
        cursor.execute(sql, schemas)
        result = cursor.fetchall()
        return [i[0] for i in result]

    def tables(self, schema=None):
        """Returns a list of tables contained in the database to which the
        class is currently attached.

        If specified, schemas should be an iterable of schemas from which the
        tables should be gathered.
        """
        sql = '''select tablename
                 from pg_tables
        '''
        if schema:
            sql += "where schemaname = %s"
        cursor = self.conn.cursor()
        cursor.execute(sql, (schema, ))
        result = cursor.fetchall()
        return [i[0] for i in result]

class Relation:

    conn = psycopg.connect(database="demo")

    def __init__(self, **kwargs):
        tablename = self.__class__.__name__
        sql = self.render_query(view=tablename, pkey=kwargs)
        cursor = self.execute(sql, kwargs)
        result = cursor.fetchone()
        self.data = {}
        for key, value in zip([i[0] for i in cursor.description], result):	
            self.data[key] = value

    def render_query(self, view=None, pkey=None):
        template = Template('''
        select * 
        from $view
        where 
        #for $key, $val in $pkey.iteritems()
        $key = %($key)s
        #end for
        ''', [locals()])
        return template.respond()

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
    def __getitem__(self, name):
        if name in self.data:
            return self.data[name]

    @classmethod
    def description(cls):
        """Returns a description of this relations attributes

        This method simply returns the description attribute from the
        DB API cursor object.  This is a sequence of 7 item sequences
        of the form (name, type_code, display_size, internal_size, 
        precision, null_ok) of which only the first two items are
        guaranteed.
        """
        cursor = cls.execute('''select * from %s
                                limit 1''' % cls.__name__)
        return cursor.description


    @classmethod
    def selectAll(cls):
        """A convenience method for selecting an entire relation from
        the database (although we simply forward the call to the more
        general execute)
        """
        return cls.execute("select * from %s" % cls.__name__)
    
    @classmethod
    def execute(cls, template, params=None, commit=True):
        """Executes the specified statement and returns a copy of the cursor
        """
        cursor = cls.conn.cursor()
        cursor.execute(template, params) #execute stmt returns None
        commit and  cls.conn.commit()
        return cursor

    @classmethod
    def insert(cls, mapping):
        """Attempts to insert the specified key value mapping into this table
        """
        keys_fmt = map(lambda x: "%%(%s)s" % x, mapping.keys())
        template = """insert into %(table)s (%(keys)s)
            values (%(values)s);""" % { 'table': cls.__name__, 
                                        'keys': ", ".join(mapping.keys()),
                                        'values': ", ".join(keys_fmt) }
        cls.execute(template, mapping)


if __name__ == '__main__':
    #replace contact with table in your database
    conn = psycopg.connect(database="demo")
    model = Model(conn)
    Contacts = model.contacts
    print Contacts.description   #lists your table attributes
    c = Contacts(id=9)           #c now represents a row in your db
    print c.email                #only if there exists an email attribute
    print c['email']

    cursor = model.contact.selectAll()
    results = cursor.fetchall()
    
