#updated 8/27/2014
import win32com.client
connection = win32com.client.Dispatch(r'ADODB.Connection')

#Constants
adStateOpen = 1


class Connection:
    def __init__(self, servername, username='', password='', db=''):
        self.connection = connection
        self.version = '';
        self.servername = servername;
        self.username = username;
        self.password = password;
        self.defdb = db;
        self.constr = '';
        if db == '':
            self.defdb = 'master'
        self.connected = 0

        if username == '':
            self.constr = "Provider=SQLOLEDB.1;Data Source=" + self.servername + ";Trusted_Connection=yes; database=" + self.defdb
        else:
            self.constr = "Provider=SQLOLEDB.1;Data Source=" + self.servername + ";uid=" + username + ";pwd=" + password + "; database=" + self.defdb

        #test connection:
        s = "set nocount on select name from master..syslogins where name = 'sa'"
        connection.Open(self.constr)
        if connection.State == adStateOpen:
            self.connected = 1

        try:
            c = Cursor()
            c.servername = servername
            c.username = username
            c.password = password
            c.defdb = db
            c.constr = self.constr
            self.cursor = c
        except IndexError:
            self.connected = 0
            print("Could not connect")

    def commit(self):
        "this is here for compatibility"
        pass

    def close(self):
        self = None
        return self


class Cursor:
    def __init__(self):
        self.records = []
        self.rowid = 0
        self.fieldnames = []
   
    def execute(self,sql):
        self.recordset = connection.execute(sql)
        self.records = []
        self.fieldnames = []

        for x in range(self.recordset.Fields.Count):
            self.fieldnames.append(self.recordset.Fields.Item(x).Name)

        #Need the try for not select type of sql, like updates, inserts
        values_list = []
        try:
            data = self.recordset.GetRows()
            self.rowcount = len(data[0])
            for y in range(0, self.rowcount):
                for x in data:
                    values_list.append(x[y])
                self.records.append(tuple(values_list))
                values_list = []
            self.records = tuple(self.records)
        except UnboundLocalError:
            pass
        except:
            pass

    def fetchall(self):
        lst = []
        try:
            for x in self.records:
                lst.append(x)
        except IndexError:
            pass
        return lst

    def fetchone(self):
        i = self.rowid
        j = i + 1
        self.rowid = j
        try:
            return tuple(self.records[i])
        except IndexError:
            pass

if __name__ == '__main__':
    c = Connection('(local)\sql2014', db='AdventureWorks2012')
    print("Connection string: " + c.constr)
    if c.connected == 1:
        print("Connected OK")
    cu = c.cursor
    lst = cu.execute('select top 10  * from Person.Person')
    print("list of columns:")
    print(cu.fieldnames)
    print('rowcount=' + str(cu.rowcount))
    print('select top 10  * from Person.Person')
    rows = cu.fetchall()
    for x in rows:
        print(x)

    print('Bringing records one by one')
    cu.rowid = 5
    rows = cu.fetchone()
    print(rows)
    rows = cu.fetchone()
    print(rows)

    print('Doing an update changing FirstName')
    cu = c.cursor
    FirstName = 'Kenny'
    BusinessEntityID = '1'
    cu.execute("update Person.Person set FirstName ='" + FirstName + "' where BusinessEntityID = " + BusinessEntityID)
    print('Reading record')
    lst = cu.execute('select * from Person.Person where BusinessEntityID = 1')
    rows = cu.fetchall()
    print(rows)
    c.close()
