"""Demonstrate using ADO to get database table definitions.
A PostgreSQL create script is generated.

Author: Craig H. Anderson  craigha@attbi.com

"""
__version__ = "$Revision: 1.11 $"
__source__ = "$Header: /home/cvsroot/home/craig/swCommunityMinistry/winPyTools/adoTableDef.py,v 1.11 2001/12/28 22:40:17 craig Exp $"

# Author used this command for testing
# execfile("E:\\FoodBank\\PyTools\\adoTableDef.py")

##--- Example output
##Drop Table Visit_Date;
##Create Table Visit_Date (
##   VisitNumber integer
##   ,FoodBankID integer
##   ,Date timestamp
##   ,EstServiceValue money
##   ,Adults integer
##   ,Children integer
##   ,Gasoline money
##   ,Tokens integer
##);

import sys
import win32com.client

def sqlName( nameStr ):
    """Make a proper token out of a string with embedded spaces and special characters

    ' ' -> '_'
    '#' -> 'Num'
    
    """
    ss = nameStr.replace(" ","_")
    ss = ss.replace("#","Num")
    return ss

class InfoAboutADOField:
    """Get information about an ADO field

    Information about database types is added manually to __init__()
    
    type constants from the Microsoft ActiveX Data Objects 2.7 Library:
	adBoolean                     =0xb        # from enum DataTypeEnum
	adCurrency                    =0x6        # from enum DataTypeEnum
	adDate                        =0x7        # from enum DataTypeEnum
	adDBTimeStamp                 =0x87       # from enum DataTypeEnum
	adInteger                     =0x3        # from enum DataTypeEnum
	adLongVarWChar                =0xcb       # from enum DataTypeEnum
	adVarWChar                    =0xca       # from enum DataTypeEnum

    The target database is PostgreSql.  Changes may be necessary for other
    databases.

    """
    def __init__(self,adoField):
        """Get name and type information from adoField"""
        self.name = None
        self.adoType = None
        self.adoLen = None
        self.sqlString = None # For sql create table

        if adoField.Type == win32com.client.constants.adInteger:
            self.name = adoField.Name
            self.adoType = adoField.Type # 3
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'integer'
            return
        if adoField.Type == win32com.client.constants.adCurrency:
            self.name = adoField.Name
            self.adoType = adoField.Type # 6
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'money'
            return
        if adoField.Type == win32com.client.constants.adDate:
            self.name = adoField.Name
            self.adoType = adoField.Type # 7
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'timestamp'
            return
        if adoField.Type == win32com.client.constants.adBoolean:
            self.name = adoField.Name
            self.adoType = adoField.Type # 11
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'boolean'
            return
        if adoField.Type == win32com.client.constants.adDBTimeStamp:
            self.name = adoField.Name
            self.adoType = adoField.Type # 135
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'timestamp'
            return
        if adoField.Type == win32com.client.constants.adVarWChar:
            self.name = adoField.Name
            self.adoType = adoField.Type # 202
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'varchar(%d)' % self.adoLen
            return
        if adoField.Type == win32com.client.constants.adLongVarWChar:
            self.name = adoField.Name
            self.adoType = adoField.Type # 203
            self.adoLen = adoField.DefinedSize
            self.sqlString = 'text'
            return
        raise "unrecognized ado field type %d" % adoField.Type

class TableInfo:
    """Use ADO Recordset to get information about the fields in a table

    name - table name
    fieldList - list of InfoAboutADOField() for each field

    """
    def __init__(self,adoConnection,tableName):
        self.name = tableName
        self.fieldList = []
        
        stmt = '[%s]' % self.name
        adoRecordSet = win32com.client.Dispatch(r'ADODB.Recordset')
        adoRecordSet.Open(stmt,adoConnection,
                          win32com.client.constants.adOpenKeyset,
                          win32com.client.constants.adLockOptimistic)
        for adoField in adoRecordSet.Fields:
            self.fieldList.append(InfoAboutADOField(adoField))
        return

class AdoTableDef:
    """Demonstrate using ADO to get database table definitions.

    """
    def __init__(self):
        self.connectionString = None # set by AdoTableDef.open()
        self.adoConnection = None # set by AdoTableDef.open()
        self.tableNames = [] # set by AdoTableDef.loadTablenames()
        self.tableInfo = None # set by AdoTableDef.genTableDef()
        return
    def genAllTableDefs(self,printObj=sys.stdout):
        """Print sql describing all the tables in self.tableNames[]
        Must call AdoTableDef.open() and AdoTableDef.loadTableNames() first
        """
        for tbl in self.tableNames:
            self.genTableDef(tbl,printObj)
        return self.tableInfo # for the last table
    def genTableDef(self,tableName,printObj=sys.stdout):
        """Print sql describing table tableName
        Must call AdoTableDef.open() and AdoTableDef.loadTableNames() first
        """
        self.tableInfo = TableInfo(self.adoConnection,tableName)
        print >> printObj,"Drop Table %s;" % sqlName(tableName)
        print >> printObj,"Create Table %s (" % sqlName(tableName)
        ii = 0
        for field in self.tableInfo.fieldList:
            fmt = "%s %s"
            if ii > 0:
                fmt = "," + fmt
            fmt = "   " + fmt
            print >> printObj,(fmt % (sqlName(field.name),field.sqlString))
            ii = ii + 1
        print >> printObj,");"
        return self.tableInfo
    def loadTableNames(self):
        """Use ADOX Catalog object to get a list of table Names
        on the currently open ADO connection
        Must call AdoTableDef.open() first
        """
        catalog = win32com.client.Dispatch(r'ADOX.Catalog')
        catalog.SetActiveConnection(self.adoConnection)
        self.tableNames = []
        for adoTable in catalog.Tables:
            if adoTable.Type == 'TABLE':
                self.tableNames.append(adoTable.Name)
        return self.tableNames
    def open(self,connectionStr):
        """Open an ADO connection using connectionStr
        """
        self.connectionString = connectionStr
        self.adoConnection = win32com.client.Dispatch(r'ADODB.Connection')
        self.adoConnection.Open(self.connectionString)
        return self.adoConnection

if __name__ == '__main__':
    """Sample program used by the author"""
    tableDef = AdoTableDef()

    # reading from a Jet mdb file
    mdbFilePath = "E:\\FoodBank\\Export20011222\\Export20011222.mdb"
    connectionStr = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s;' % mdbFilePath

    tableDef.open(connectionStr) # tableDef.adoConnection holds the open ADO connection
    tableDef.loadTableNames() # tableDef.tableNames[] has a list of tables on the open ADO connection
    #tableDef.genTableDef(tableDef.tableNames[3]) # Picked a table to see definiton
    tableDef.genAllTableDefs(open('C:\\glop.txt','w'))
    #tableDef.genTableDef(tableDef.tableNames[3],open('C:\\glop.txt','w')) # try output to file
