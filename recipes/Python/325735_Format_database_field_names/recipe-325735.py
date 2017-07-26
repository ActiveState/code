# XLfields.py - M.Keranen (mksql@yahoo.com) [10/29/2004]
# -------------------------------------------------------------------------------
# Formats first row cells of an MS Excel (tm) sheet to allow for proper importing
# into databases. Assumes field names in top row, beginning with leftmost column.

import os, string, sys
from win32com.client import Dispatch

namefmt = '0'
namelen = 128

if len(sys.argv)<2:
	print "\nUsage: XLfields.py path/infile.xls [Field name format] [Max field name width]"
	print "\nFormat: 0 = TitleCasedWords"
	print "        1 = Titlecased_Words_Underscored"
	print "        2 = lowercase_words_underscored"
	print "        3 = Words_underscored_only (leave case as in source)"
	sys.exit()
else:
	if len(sys.argv)==2: dummy, xlfile, = sys.argv
	elif len(sys.argv)==3: dummy, xlfile, namefmt = sys.argv
	else: dummy, xlfile, namefmt, namelen = sys.argv

namefmt = int(namefmt)
namelen = int(namelen)

if not os.path.exists(xlfile):
	print "\nFile %s not found." % (xlfile)

# Create string translation tables
allowed = ' _01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
delchars = ''
for i in range(255):
	if chr(i) not in allowed: delchars = delchars + chr(i)
deltable = string.maketrans(' ','_')

# Open file in Excel
xl = Dispatch("Excel.Application")
xl.Visible = 1
xl.Workbooks.Open(xlfile,0)
xls = xl.Sheets(1)
nc = xls.UsedRange.Columns.Count + 1

# Format column names
cols = []
for c in range(1,nc):
	# Format column name to remove unwanted chars
	col = string.strip(str(xls.Cells(1,c).Value))
	col = col[:namelen]
	col = col.translate(deltable,delchars)
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
	cols.append(dupcol)
	print "%s -> %s" % (xls.Cells(1,c).Value,dupcol)
	xls.Cells(1,c).Value = dupcol

# Save file under new name. Comment out to leave file open in Excel
#xlname = os.path.basename(xlfile).split('.')[0]
#outfile = os.path.dirname(xlfile) + '\\' + xlname + '.new.xls'
#xl.ActiveWorkbook.SaveAs(Filename=outfile)
#xl.Quit()

sys.exit()
