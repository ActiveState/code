import dtuple
import mx.ODBC.Windows as odbc

flist = ["Name", "Num", "LinkText"]

descr = dtuple.TupleDescriptor([[n] for n in flist])

conn = odbc.connect("HoldenWebSQL") # Connect to a database
curs = conn.cursor()                # Create a cursor

sql = """SELECT %s FROM StdPage
            WHERE PageSet='Std' AND Num<25
            ORDER BY PageSet, Num""" % ", ".join(flist)
print sql
curs.execute(sql)
rows = curs.fetchall()

for row in rows:
    row = dtuple.DatabaseTuple(descr, row)
    print "Attribute: Name: %s Number: %d" % (row.Name, row.Num or 0)
    print "Subscript: Name: %s Number: %d" % (row[0], row[1] or 0)
    print "Mapping:   Name: %s Number: %d" % (row["Name"], row["Num"] or 0)

conn.close()
