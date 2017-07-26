from java.lang import *
from java.sql import *

'''
Path to the excel file.This can be an absolute path or the relative path. 
In case of relative path, relativity starts from where the script is run from.
'''
excelfile="values.xls"

Class.forName("sun.jdbc.odbc.JdbcOdbcDriver")

cnExcel=DriverManager.getConnection("jdbc:odbc:Driver={Microsoft Excel Driver (*.xls)};DBQ=%s;READONLY=true}" % excelfile,"","")

'''
Sheet1 is the name of the workbook in the excel sheet.All the 
values in the columns of first row will be taken as the 
column names.
'''
rs=cnExcel.createStatement().executeQuery("SELECT * FROM [Sheet1$])

while rs.next():
'''
The number in getString(i) method is dependent on the number of columns
available in the excel sheet
'''
    print rs.getString(1)

'''
Play safe.Close the connection and the recordset.
'''
rs.close()
cnExcel.close()
