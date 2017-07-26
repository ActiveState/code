# csv2tbl.py - M.Keranen (mksql@yahoo.com) [10/14/2004]
# ------------------------------------------------------------------------
# Read a CSV file (exported from Excel), and generate an SQL statement
# to create a matching table structure (by field names and widths only).
# Expects sheet to start in cell A1, column names in first row:
# Suggested Excel export steps:
# 	1) Delete blank leading rows and columns to bring start of sheet to A1
# 	2) Select all cells, left justify, Format->Column->Auto Fit Selection
#	3) Save as file type .CSV
# -------------------------------------------------------------------------

import csv, os, string, sys

if len(sys.argv)<2:
	print "\nUsage: csv2tbl.py path/datafile.csv (0,1,2,3 = column name format):"
	print "\nFormat: 0 = TitleCasedWords"
	print "        1 = Titlecased_Words_Underscored"
	print "        2 = lowercase_words_underscored"
	print "        3 = Words_underscored_only (leave case as in source)"
	sys.exit()
else:
	if len(sys.argv)==2:
		dummy, datafile, = sys.argv
		namefmt = '0'
	else: dummy, datafile, namefmt = sys.argv

namefmt = int(namefmt)
#outfile = os.path.basename(datafile)
tblname = os.path.basename(datafile).split('.')[0]
outfile = os.path.dirname(datafile) + '\\' + tblname + '.sql'

# Create string translation tables
allowed = ' _01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
delchars = ''
for i in range(255):
	if chr(i) not in allowed: delchars = delchars + chr(i)
deltable = string.maketrans(' ','_')

# Create list of column [names],[widths]
reader = csv.reader(file(datafile),dialect='excel')
row = reader.next()
nc = len(row)
cols = []
for col in row:
	# Format column name to remove unwanted chars
	col = string.strip(col)
	col = string.translate(col,deltable,delchars)
	fmtcol = col
	if namefmt < 3:
		# Title case individual words, leaving original upper chars in place
		fmtcol = ''
		for i in range(len(col)):
			if col.title()[i].isupper(): fmtcol = fmtcol + col[i].upper()
			else: fmtcol = fmtcol + col[i]
	if namefmt == 2: fmtcol = col.lower()
	if namefmt == 0: fmtcol = string.translate(fmtcol,deltable,'_')   # Remove underscores
	
	d = 0
	dupcol = fmtcol	
	while dupcol in cols:
		d = d + 1
		dupcol = fmtcol + '_' + str(d)
	cols.append([dupcol,1])

# Determine max width of each column in each row
rc = 0
for row in reader:
	rc = rc + 1
	if len(row) == nc:
		for i in range(len(row)):
			fld = string.strip(row[i])
			if len(fld) > cols[i][1]:
				cols[i][1] = len(fld)
	else: print 'Warning: Line %s ignored. Different width than header' % (rc)

print

sql = 'CREATE TABLE %s\n(' % (tblname)
for col in cols:
	sql = sql + ('\n\t%s NVARCHAR(%s) NULL,' % (col[0],col[1]))
sql = sql[:len(sql)-1] + '\n)'

sqlfile = open(outfile,'w')
sqlfile.write(sql)
sqlfile.close

print '%s created.' % (outfile)
