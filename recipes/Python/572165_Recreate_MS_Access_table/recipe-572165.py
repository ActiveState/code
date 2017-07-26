"""
jetout.py - Reconstructs a given table from a Jet (MS Access) file in SQLite,
storing created table on disk; uses win32com to get to DAO 3.6 (Office 2000),
and uses sqlite3.  To ensure index names are unique to the entire database,
names of recreated indexes are prefixed with the table name.

Date/Time typed columns are reformatted to ISO's yyyy-mm-dd, and may be recalled
as datetime.date types using the built-in DATE converter in pysqlite's
converters dictionary, if the database is opened with the argument
'detect_types=sqlite3.PARSE_DECLTYPES' in the 'connect' statement.

To modify this module to import Date/Time type as datetime.datetime instead
of datetime.date:  change 'DATE' to 'TIMESTAMP' for CREATE TABLE, and modify
last line of sepdate function to include 'timepart'.

Usage:
sqlitefromjet("input.mdb", "input table name", "output.db"
[, # of rows to fetch/commit at a time])
"""
def sqlitefromjet(mdb, tbl, sqlite_db, fetchsize=1000):
        import win32com
        from win32com import client
        import sqlite3
        from itertools import imap, izip
        engine = win32com.client.Dispatch("DAO.DBEngine.36") # Office 2000
        db = engine.OpenDatabase(mdb)
        table = db.OpenRecordset(tbl)
        connection = sqlite3.connect(sqlite_db)
        cursor = connection.cursor()
        if tbl.find(' ') != -1 and tbl[:1] != '[':
                tbl = '[' + tbl + ']' # bracket table names with spaces
        # build SQL statement to create table
        createStr = 'CREATE TABLE ' + tbl + ' (' 
        fieldrange = range(table.Fields.Count)
        isType = [] # check field types (use to make ISO date from Date/Time)
        pkf = False # look for AutoNumber PK field to make INTEGER PRIMARY KEY
        havePK = False
        for tdef in db.TableDefs:
                if tdef.Name == table.Name:
                        tblDef = tdef # grab TableDef object for its indexes
                        break
        for idx in tblDef.Indexes:
                if idx.Primary:
                        for idxf in idx.Fields:
                                if pkf:
                                        pkf = False
                                        break
                                pkf = idxf.Name # grab PK field, if only one
                        break # found the PK; all done
        for field in fieldrange:
                createStr = createStr + '[' + table.Fields(field).Name + ']'
                ftype = table.Fields(field).Type # get int representing type
                if ftype == 4:
                        if pkf:
                                if table.Fields(field).Name == pkf:
                # if field was AutoNumber PK, will still autoincrement
                                        createStr += ' INTEGER PRIMARY KEY, '
                                        havePK = True
                        else:
                                createStr += ' INTEGER, '
                        isType.append(1)
                elif ftype in (2,3):
                        isType.append(1) # number
                        createStr += ' INTEGER, '
                elif ftype in (5,6,7,20):
                        if ftype == 5:
                                isType.append(3) # currency type
                        else:
                                isType.append(1) # number
                        createStr += ' NUMERIC, '
                elif ftype == 8:
                        isType.append(2) # date
                        createStr += ' DATE, ' # (or TIMESTAMP)
                else:
                        isType.append(0) # text
                        createStr += ' TEXT, '
                if table.Fields(field).Required:
                        createStr = createStr[:-2] + ' NOT NULL, '
        createStr = createStr[:-2] + ');'
        cursor.execute(createStr) # create table
        stmt = "INSERT INTO " + tbl + " VALUES(" # build INSERT for executemany
        for fieldnum in fieldrange:
                stmt += "?, "
        stmt = stmt[:-2] + ")"
        df = [x for x in fieldrange if isType[x] == 2] # date column offsets
        cf = [x for x in fieldrange if isType[x] == 3] # currency column offsets
        lastSet = False
        while not lastSet:
                # fetch 'fetchsize' records at a time (default of 1,ooo)
                fetched = map(list, table.GetRows(fetchsize)) # in mutable form
                fetchnum = len(fetched[0]) # get actual number of rows fetched
                print "\tFetched " + "%s" % fetchnum + " rows"
                # check if all 'fetchsize' rows fetched...
                if fetchnum < fetchsize:    
                        lastSet = True # ...last set (or read error) if not
                for x in df:
                        fetched[x] = imap(sepdate, fetched[x]) # yyyy-mm-dd
                for x in cf:
                        fetched[x] = imap(conv_curr, fetched[x]) # get currency
                rows = izip(*fetched) # put [fields][rows] into [rows][fields]
                cursor.executemany(stmt, rows) # INSERT one fetch
                connection.commit() # commit one transaction per fetch
        print "INSERTs complete - creating indexes..." 
        for idx in tblDef.Indexes:
                newName = table.Name + idx.Name 
                if idx.Unique:
                        if havePK and idx.Primary:
                                continue # already have unique index if int PK
                        else:
                                createStr = "CREATE UNIQUE INDEX [" + \
                                            newName + "] ON " + tbl + "("
                else:
                        createStr = "CREATE INDEX [" + newName + "] ON " + \
                                    tbl + "("
                for idxf in idx.Fields:
                        createStr += "[" + idxf.Name + "], "
                createStr = createStr[:-2] + ");"
                cursor.execute(createStr) # add an index
        print "ok - all done"
        cursor.close()
        connection.close()
        table.Close()
        db.Close()

def sepdate(dt):
        """sepdate('%m/%d/%y %H:%M:%S') -> '%Y-%m-%d'

Return ISO-format yyyy-mm-dd date from Access-formatted Date/Time."""
        dt = "%s" % dt
        if dt.find(" ") != -1:
                datepart, timepart =  dt.split(" ")
        else:
                return None
        month, day, year = datepart.split("/")
        if int(year) <= 29:
                year = '20' + year # make same assumptions about 2-digit
        elif int(year) <= 99:
                year = '19' + year # years as Access' Short Date format
        return year + "-" + month + "-" + day  # + " " + timepart # TIMESTAMP

def conv_curr(curr):
        """conv_curr(Access currency-typed field) -> float

Return a float from MS Access currency datatype, which is a fixed-point integer
scaled by 10,000"""
        return float(curr[1])/10000 # convert fixed-point int to float
