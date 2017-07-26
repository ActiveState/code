import dbi,odbc

class DBCore:
    """Basic DB access."""

    def __init__(self,dbname):
        self._DB = odbc.odbc(dbname)
        self._cur = self._DB.cursor()

    def executeUpdate(self,sql,*parms):
        self._cur.execute(sql,*parms)

    def executeQuery(self,sql,*parms,**kws):
        strip = 0
        try:
            strip = kws['strip']
        except KeyError:
            pass

        self._cur.execute(sql,*parms)
        results = self._cur.fetchall()

        if strip:
            # Remove extraneous sequence nesting.
            if len(results) == 1 and len(results[0]) == 1:
                return results[0][0]

        return results

    def execute(self,sql,*args,**kws):
        if sql[0:6] == "select":
            return self.executeQuery(sql,*args,**kws)
        else:
            self.executeUpdate(sql,*args,**kws)

class DBAttrib(DBCore):
    """Provides magic for getting and setting attributes
    in the database via ODBC."""

    def __init__(self,dbname,table,cols,where,whereparms):
        """
        dbname: ODBC data source name.
        table: DB table name.
        cols:  map of attribute names to names of columns in table.
        where: where clause of query to fetch this object's table data.
        whereparms: sequence containing parameters to <where>.
        """
        self.__dict__['_db_cols'] = cols
        self._db_table = table
        self._db_where = where
        self._db_whereparms = whereparms
        DBCore.__init__(self,dbname)

    def __setattr__(self,attr,value):
        """Look for a _set_attr method. If found, use it. Otherwise, if the
        attribute is a DB column, use ODBC. Otherwise, set in the
        object dict."""
        try:
            setmethod = getattr(self,"_set_"+attr)
            return apply(setmethod,(value,))
        except AttributeError:
            pass
        if attr in self._db_cols.keys():
            self._db_set_attr(attr,value)
            return
        self.__dict__[attr] = value

    def __getattr__(self,attr):
        """Ignore _set_ and _db_ attribs. If there's a _get_attr method,
        use it. Otherwise, if it's a DB column, use ODBC."""
        if attr[0:5] == "_set_":
            raise AttributeError
        if attr[0:5] == "_get_":
            raise AttributeError
        if attr[0:4] == "_db_":
            raise AttributeError
        try:
            getmethod = getattr(self,"_get_"+attr)
            return apply(getmethod)
        except AttributeError:
            pass
        if attr in self._db_cols.keys():
            return self._db_get_attr(attr)
        raise AttributeError

    def _db_get_attr(self,attr):
        """ Get attr from the database. """
        attr = self._db_cols[attr]
        sql = "select \"%s\" from \"%s\" %s"%(attr,self._db_table,
                                              self._db_where)
        return self.execute(sql,self._db_whereparms,strip=1)

    def _db_set_attr(self,attr,value):
        """ Set attr in the database. """
        attr = self._db_cols[attr]
        sql = "update \"%s\" set \"%s\" = ? %s"%(self._db_table,
                                                 attr,self._db_where)
        self.execute(sql,(value,)+self._db_whereparms)


# Example: the "Student" table has columns "Last Name", "First Name",
# "Middle", and "Customer ID."
class Student(DBAttrib):

    def __init__(self,dbname,student_id):
        DBAttrib.__init__(self,
                          
                          dbname,
                          
                          'Student',
                          
                          {'lastname':'Last Name',
                           'firstname':'First Name',
                           'middle':'Middle',
                           'custid':'Customer ID'},
                          
                          'where "Customer ID" = ?',
                          
                          (student_id,))

stu = Student("MYDB","999-9999")

# Fetch DB data.
print stu.custid,stu.lastname,stu.firstname,stu.middle

# Update DB data.
stu.middle = "X"
