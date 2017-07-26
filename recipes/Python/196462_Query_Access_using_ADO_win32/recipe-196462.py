#ADO.py
#!C:\Python22\python
print "Content-type:text/html\n\n"
import win32com.client

NUM_ROWS=2155
#db='E:\Workarea\\Northwind.mdb'
db='C:\\Program Files\\Microsoft Office\\Office\\Samples\\Northwind.mdb'
def connect(qry):
	con=win32com.client.Dispatch('ADODB.Connection')
	rs=win32com.client.Dispatch('ADODB.recordset')
	con.Open("Provider=Microsoft.Jet.OLEDB.4.0; Data Source="+db)
	sql=qry +";"
	rs=con.Execute(sql)
	con.Close
	return rs

def display (NUM_ROWS):
	print "<table border=1>"
	print "<th>Order ID</th>"
	print "<th>Product</th>"
	print "<th>Unit Price</th>"
	print "<th>Quantity</th>"
	print "<th>Discount</th>"
	for k in range(0,NUM_ROWS):
		print "<tr>"
		for i in s:
			print "<td>",i[k],"</td>"
		print "</tr>"

	print "</table>"

rs=win32com.client.Dispatch('ADODB.recordset')
rs=connect("select * from [Order details]")
s=rs[0].GetRows(NUM_ROWS)
display(NUM_ROWS)
rs[0].Close
