dbh = dbi.connect("DBI:mysql:database=mydatabase", "myysername",
                  RaiseError = 1,
                  PrintError = 0,
                  AutoCommit = 1,
                 )

try:
    dbh["AutoCommit"] = 0
except:
    print "Can't turn off AutoCommit"

sth = dbh.prepare("select * from foo limit 5")
sth.execute()

while 1:
        row = sth.fetchrow_tuple()
        if not row: break
        print row

dbh.disconnect()
