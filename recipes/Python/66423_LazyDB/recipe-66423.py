"""The LazyDB module transparently wraps any DB API compliant
interface (DCOracle, odbc, cx_oracle, etc.) and provides:
1. lazy evaluation and caching of database connections
2. one-step query facility with data access by column name

Example:

import LazyDB, cx_Oracle
myDB = LazyDB.Connection(cx_Oracle.connect, 'user/passwd@server')
pctSQL = 'SELECT * FROM all_tables WHERE pct_used >= %(pct)s'
hogs = [(r.table_name, r.pct_used) for r in myDB(pctSQL, pct=90)]"""

class Connection:
    """Lazy proxy for database connection."""
    
    def __init__(self, factory, *args, **keywords):
        """Initialize with factory method to generate DB connection
        (e.g. odbc.odbc, cx_Oracle.connect) plus any positional and/or
        keyword arguments required when factory is called."""
        self.__cxn = None
        self.__factory = factory
        self.__args = args
        self.__keywords = keywords
    
    def __getattr__(self, name):
        if self.__cxn is None:
            self.__cxn = self.__factory(*self.__args, **self.__keywords)
        return getattr(self.__cxn, name)

    def close(self):
        if self.__cxn is not None:
            self.__cxn.close()
            self.__cxn = None

    def __call__(self, sql, **keywords):
        """Execute sql query and return results. Optional keyword
        args are '%' substituted into query beforehand."""
        cursor = self.cursor()
        cursor.execute(sql % keywords)
        return RecordSet(
            [list(x) for x in cursor.fetchall()],
            [x[0].lower() for x in cursor.description]
            )


class RecordSet:
    """Wrapper for tabular data."""

    def __init__(self, tableData, columnNames):
        self.data = tableData
        self.columns = columnNames
        self.columnMap = {}
        for name,n in zip(columnNames, xrange(10000)):
            self.columnMap[name] = n
        
    def __getitem__(self, n):
        return Record(self.data[n], self.columnMap)

    def __setitem__(self, n, value):
        self.data[n] = value

    def __delitem__(self, n):
        del self.data[n]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return '%s: %s' % (self.__class__, self.columns)


class Record:
    """Wrapper for data row. Provides access by
    column name as well as position."""

    def __init__(self, rowData, columnMap):
        self.__dict__['_data_'] = rowData
        self.__dict__['_map_'] = columnMap

    def __getattr__(self, name):
        return self._data_[self._map_[name]]

    def __setattr__(self, name, value):
        try:
            n = self._map_[name]
        except KeyError:
            self.__dict__[name] = value
        else:
            self._data_[n] = value

    def __getitem__(self, n):
        return self._data_[n]

    def __setitem__(self, n, value):
        self._data_[n] = value

    def __getslice__(self, i, j):
        return self._data_[i:j]

    def __setslice__(self, i, j, slice):
        self._data_[i:j] = slice

    def __len__(self):
        return len(self._data_)
        
    def __str__(self):
        return '%s: %s' % (self.__class__, repr(self._data_))
