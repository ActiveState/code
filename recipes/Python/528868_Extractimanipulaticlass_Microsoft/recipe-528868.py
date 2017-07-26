"""
Enables you to interrogate an Access database, run queries, and get 
results.
ADODB = Microsoft ActiveX Data Objects reference
ADOX = Microsoft ADO Ext
Great reference for ADODB is:
http://www.codeguru.com/cpp/data/mfc_database/ado/article.php/c4343/
Originally just an API wrapped around Douglas Savitsky's code at 
http://www.ecp.cc/pyado.html
Recordset iterator taken from excel.py in Nicolas Lehuen's code at 
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440661
Handling of field types taken from Craig Anderson's code at 
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/104801
An alternative approach might be 
http://phplens.com/lens/adodb/adodb-py-docs.htm
v1.0.5 - added ability to add a primary-foreign table relationship
v1.0.4 - added ability to delete a relationship by name
v1.0.3 - add ability to delete a named index, and to 
    close (release) a table.
v1.0.2 - added Close method to connection (recordset 
    automatically closes self already)
v1.0.1 - added DOUBLE and reordered data const mappings
"""
#To get constant values, open Access, make sure ADODB and ADOX are references, 
#  open library, and look at globals
AD_OPEN_KEYSET = 1
AD_LOCK_OPTIMISTIC = 3
AD_KEY_FOREIGN = 2
AD_RI_CASCADE = 1
INTEGER = 'integer'
SMALLINT = 'smallint'
UNSIGNEDTINYINT = 'unsignedtinyint'
CURRENCY = 'currency'
DATE = 'date'
BOOLEAN = 'boolean'
TIMESTAMP = 'timestamp'
VARCHAR = 'varchar'
LONGVARCHAR = 'longvarchar'
SINGLE = 'single'
DOUBLE = 'double'

INDEX_UNIQUE = 'unique'
INDEX_NOT_UNIQUE = 'notunique'
INDEX_PRIMARY = 'indexprimary'
INDEX_NOT_PRIMARY = "indexnotprimary"

import win32com.client
#Must run makepy once - 
#see http://www.thescripts.com/forum/thread482449.html e.g. the following 
#way - run PYTHON\Lib\site-packages\pythonwin\pythonwin.exe (replace 
#PYTHON with folder python is in).  Tools>COM Makepy utility - select 
#library named Microsoft ActiveX Data Objects 2.8 Library (2.8) and 
#select OK. Microsoft ActiveX Data Objects Recordset 2.8 Library (2.8)

class AccessDb:
    "Interface to MS Access database"
    
    def __init__(self, data_source, user, pwd="''", mdw="''"):
        """Returns a connection to the jet database
        NB use .Close() to close (NB title case unlike closing a file)"""
        self.connAccess = win32com.client.Dispatch(r'ADODB.Connection')
        """DSN syntax - http://support.microsoft.com/kb/193332 and 
        http://www.codeproject.com/database/connectionstrings.asp?
        df=100&forumid=3917&exp=0&select=1598401"""
        DSN = """PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s;
            USER ID=%s;PASSWORD=%s;Jet OLEDB:System Database=%s;""" % \
            (data_source, user, pwd, mdw)
        #print DSN
        try:
            self.connAccess.Open(DSN)
        except Exception:
            raise Exception, "Unable to open MS Access database " + \
                "using DSN: %s" % DSN
    
    def getConn(self):
        "Get connection"
        return self.connAccess
    
    def closeConn(self):
        "Close connection"
        self.connAccess.Close()
    
    def getRecordset(self, SQL_statement, dict=True):
        "Get recordset"
        return Recordset(self.connAccess, SQL_statement, dict=dict)
    
    def getTableNames(self):
        "Get list of tables.  NB not system tables"
        cat = win32com.client.Dispatch(r'ADOX.Catalog')
        cat.ActiveConnection = self.connAccess
        alltables = cat.Tables
        tab_names = []
        for tab in alltables:
            if tab.Type == 'TABLE':
                tab_names.append(tab.Name)
        return tab_names
    
    def getTables(self):
        "Get dictionary of table objects - table name is the key"
        tab_names = self.getTableNames()
        tabs = {}
        for tab_name in tab_names:
            tabs[tab_name] = Table(self.connAccess, tab_name)
        return tabs
    
    def runQuery(self, SQL_statement):
        "Run SQL_statement"
        cmd = win32com.client.Dispatch(r'ADODB.Command')
        cmd.ActiveConnection = self.connAccess
        cmd.CommandText = SQL_statement
        cmd.Execute()

    def deleteIndex(self, tab_name, idx_name):
        """
        Delete index by name.
        NB cannot delete an index if a table is locked.
        Or if it is part of a relationship (I would expect).  
        Release (close) it first.
        """
        cat = win32com.client.Dispatch(r'ADOX.Catalog')
        cat.ActiveConnection = self.connAccess
        index_coll = cat.Tables(tab_name).Indexes
        try:
            index_coll.Delete(idx_name)
        except Exception, e:
            raise Exception, "Unable to delete index - if table is " + \
                "locked, make sure you release (close) it first.  " + \
                "Orig error: " + str(e)
        cat = None
    
    def addRelationship(self, tab_foreign_name, tab_foreign_key, 
                        tab_primary_name, tab_primary_key,
                        rel_name, cascade_del=False, 
                        cascade_update=False):
        """
        Add primary table-foreign table relationship        
        """
        tabs = [tab_foreign_name, tab_primary_name]
        for tab in tabs:        
            if tab not in self.getTableNames():
                raise Exception, "Table \"%s\" is not in this database" \
                    % tab
        cat = win32com.client.Dispatch(r'ADOX.Catalog')
        cat.ActiveConnection = self.connAccess
        tbl_foreign = cat.Tables(tab_foreign_name)
        new_key = win32com.client.Dispatch(r'ADOX.Key')
        try:
            new_key.Name = rel_name
            new_key.Type = AD_KEY_FOREIGN
            new_key.RelatedTable = tab_primary_name
            new_key.Columns.Append(tab_foreign_key)
            new_key.Columns(tab_foreign_key).RelatedColumn = tab_primary_key
            if cascade_del:
                new_key.DeleteRule = AD_RI_CASCADE
            if cascade_update:
                new_key.UpdateRule = AD_RI_CASCADE
            tbl_foreign.Keys.Append(new_key)
        except Exception, e:
            raise Exception, "Unable to add relationship '%s'. " % \
                rel_name + "Orig error: %s" % str(e)
        finally:
            tbl_foreign = None
            cat = None
    
    def deleteRelationship(self, tab_foreign_name, rel_name):
        """
        Delete relationship by relationship name.
        Need name of "foreign" table.
        http://msdn2.microsoft.com/en-us/library/aa164927(office.10).aspx
        """
        if tab_foreign_name not in self.getTableNames():
            raise Exception, "Table \"%s\" is not in this database" % \
                tab_foreign_name
        cat = win32com.client.Dispatch(r'ADOX.Catalog')
        cat.ActiveConnection = self.connAccess
        tbl_foreign = cat.Tables(tab_foreign_name)
        tbl_keys = [x.Name for x in tbl_foreign.Keys]
        if rel_name not in tbl_keys:
            raise Exception, "\"%s\" is not in " % rel_name + \
                "relationships for table \"%s\"" % tab_foreign_name
        tbl_foreign.Keys.Delete(rel_name)
        tbl_foreign = None
        cat = None
        

class Table():
    "MS Access table object with rs, name, and index properties"
    def __init__(self, connAccess, tab_name):
        self.connAccess = connAccess
        self.rs = win32com.client.Dispatch(r'ADODB.Recordset')
        try:
            self.rs.Open("[%s]" % tab_name, self.connAccess, AD_OPEN_KEYSET, 
                         AD_LOCK_OPTIMISTIC)
        except Exception, e:
            raise Exception, "Problem opening " + \
                "table \"%s\" - " % tab_name + \
                "orig error: %s" % str(e)
        self.name = tab_name
        self.indexes = self.__getIndexes()
    
    def getFields(self):
        "Get list of field objects"
        field_names = [field.Name for field in self.rs.Fields]
        fields = []
        for field_name in field_names:
            fields.append(Field(self.rs, field_name))        
        return fields
    
    def __getIndexes(self):
        "Get list of table indexes"
        cat = win32com.client.Dispatch(r'ADOX.Catalog')
        cat.ActiveConnection = self.connAccess
        index_coll = cat.Tables(self.name).Indexes
        indexes = []
        for index in index_coll:
            indexes.append(Index(index))
        return indexes
        cat = None
        
    def close(self):
        "Close table (releasing it)"
        self.rs.Close()
        
        
class Index():
    """MS Access index object with following properties: name, 
    index type (UNIQUE or not), primary or not, and index fields - 
    a tuple of index fields in index"""
    def __init__ (self, index):
        self.name = index.Name        
        if index.Unique:
            self.type = INDEX_UNIQUE
        else:
            self.type = INDEX_NOT_UNIQUE
        self.fields = []
        for item in index.Columns:
            self.fields.append(item.Name)
        if index.PrimaryKey:
            self.primary = INDEX_PRIMARY
        else:
            self.primary = INDEX_NOT_PRIMARY
    
class Field():
    "MS Access field object with name, type, and size properties"
    def __init__ (self, rs, field_name):
        self.name = field_name
        adofield = rs.Fields.Item(field_name)
        adotype = adofield.Type
        #http://www.devguru.com/Technologies/ado/quickref/field_type.html
        if adotype == win32com.client.constants.adInteger:
            self.type = INTEGER
        elif adotype == win32com.client.constants.adSmallInt:
            self.type = SMALLINT
        elif adotype == win32com.client.constants.adUnsignedTinyInt:
            self.type = UNSIGNEDTINYINT
        elif adotype == win32com.client.constants.adSingle:
            self.type = SINGLE
        elif adotype == win32com.client.constants.adDouble:
            self.type = DOUBLE
        elif adotype == win32com.client.constants.adCurrency:
            self.type = CURRENCY
        elif adotype == win32com.client.constants.adBoolean:
            self.type = BOOLEAN
        elif adotype == win32com.client.constants.adDate:
            self.type = DATE
        elif adotype == win32com.client.constants.adDBTimeStamp:
            self.type = TIMESTAMP
        elif adotype == win32com.client.constants.adVarWChar:
            self.type = VARCHAR
        elif adotype == win32com.client.constants.adLongVarWChar:
            self.type = LONGVARCHAR
        else:
            raise "Unrecognised ADO field type %d" % adotype
        self.size = adofield.DefinedSize

def encoding(value):
    if isinstance(value,unicode):
        value = value.strip()
        if len(value)==0:
            return None
        else:
            return value.encode("mbcs") #mbcs is a Windows, locale-specific encoding
    elif isinstance(value,str):
        value = value.strip()
        if len(value)==0:
            return None
        else:
            return value 
    else:
        return value

class Recordset():
    "MS Access recordset created from a query"
    
    def __init__ (self, connAccess, SQL_statement, dict):
        self.rs = win32com.client.Dispatch(r'ADODB.Recordset')
        self.rs.CursorLocation = 3 #uses client - makes it possible to use RecordCount property
        self.rs.Open(SQL_statement, connAccess, AD_OPEN_KEYSET, 
                     AD_LOCK_OPTIMISTIC)
        self.dict = dict
 
    def getFieldNames(self):
        "Get list of field names"
        field_names = [field.Name for field in self.rs.Fields]
        return field_names
    
    def hasRows(self):
        "Does the recordset contain any rows?"
        try:
            self.rs.MoveFirst()
        except:
            return False
        return True
    
    def getCount(self):
        """
        Get record count - NB rs.CursorLocation had to be set to 
        3 (client) to enable this
        """
        try:
            return self.rs.RecordCount
        except:
            return 0
    
    def __iter__(self):
        " Returns a paged iterator by default. See paged()."
        return self.paged()
    
    def paged(self,pagesize=128):
        """ Returns an iterator on the data contained in the sheet. Each row
        is returned as a dictionary with row headers as keys. pagesize is
        the size of the buffer of rows ; it is an implementation detail but
        could have an impact on the speed of the iterator. Use pagesize=-1
        to buffer the whole sheet in memory.
        """
        try:
            field_names = self.getFieldNames()
            #field_names = [self.encoding(field.Name) for field in recordset.Fields]
            ok = True
            while ok:
                # Thanks to Rogier Steehouder for the transposing tip 
                rows = zip(*self.rs.GetRows(pagesize))                
                if self.rs.EOF:
                    # close the recordset as soon as possible
                    self.rs.Close()
                    self.rs = None
                    ok = False
                for row in rows:
                    if self.dict:
                        yield dict(zip(field_names, map(encoding,row)))
                    else:
                        yield(map(encoding, row))                
        except:
            if self.rs is not None:
                self.rs.Close()
                del self.rs
            raise
