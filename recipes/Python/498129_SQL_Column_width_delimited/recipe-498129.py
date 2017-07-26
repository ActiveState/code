# SQLColumnWidth.py - M.Keranen (mksql@yahoo.com) - 09/22/2006
# ------------------------------------------------------------
# Find max width of each character column in a delimited text file,
# and modify DDL file to max width of respective source columns.

import sys

if len(sys.argv)<2:
    print "\nUsage: %s datafile tableddl.sql" % (sys.argv[0])
    sys.exit()
else:
    dummy, datafile, sqlfile = sys.argv
    print

f = open(datafile,'r')

cw = {}
c = f.readline()
cw = cw.fromkeys(c.split(','),0)

r = 0
l = f.readline()
while l != '':
    r += 1

    col = l.split('|')
    if len(col) != len(cw): print 'Length error in row %s' % (r)
    i = 0

    for c in cw.iterkeys():
        if len(col[i]) > cw[c]: cw[c] = len(col[i])            
        i += 1
    l = f.readline()

#print cw
f.close()


# Match cw dict to CREATE TABLE statement for VARCHAR columns,
# and replace width where data is present larger than column definition

sql = open(sqlfile,'r').read()
lsql = sql.lower() # Copy of SQL to eliminate case in searches

for c in cw.iterkeys():
    
    dt = lsql.find(c)+len(c)+1
    if lsql[dt:dt+7] == 'varchar' or lsql[dt:dt+4] == 'char':
        lp = dt + lsql[dt:].find('(')+1
        rp = dt + lsql[dt:].find(')')

        # Original values
        ow = int(lsql[lp:rp])
        osql = sql[lsql.find(c):rp+1]
        
        if ow < cw[c]:
            # Update both lower cased SQL and original to maintain positions
            lsql = lsql[:lp] + str(cw[c]) + lsql[rp:]
            sql = sql[:lp] + str(cw[c]) + sql[rp:]
            print "%s ->%s" % (osql, sql[lsql.find(c)+len(c):rp+1])
        
open(sqlfile+'.new','w').write(sql)
print "\n%s written.\n" % (sqlfile+'.new')
