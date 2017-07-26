import mx.ODBC.Windows as odbc

#To find out what you can use to access the database, run this command
#datasource = odbc.DataSources()

#2 possible ways to hit an access file
driv='DRIVER={Microsoft Access Driver (*.mdb)};DBQ=c:/tmp/a.mdb'
#driv2='FILEDSN=c:/tmp/a.mdb'

conn = odbc.DriverConnect(driv)
c = conn.cursor()
c.execute ("select * from the_table_name  where columna = 'fred'")

#get column names
cols= [ i[0] for i in c.description ]
print '\n\ncols=',cols

##print '\n\n',c.fetchone()
rows = c.fetchall()
print '\n\n','length of rows: ',len(rows)

print '\n\n'
cnt = 0
for r in rows:
   cnt += 1
   print cnt,'  ',r
   if cnt > 10:
      break
