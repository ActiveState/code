'''
 Author : Alexander Baker 
 Description : Simple script that connects to a database and reads some data
 Date : 26th August 2008
 Revision : na
'''

def store_value(option, opt_str, value, parser):
    setattr(parser.values, option.dest, value)
    
def check_value(value):
    if var == "yes" or var == "y" or var =="YES" or var == "Yes":
    	return True
    else :
    	return False

def formatDateTimeDash(rawString):
	now = datetime.datetime(*time.strptime(rawString, "%Y-%m-%d %H:%M:%S.000")[0:5])	
	return "'" + now.strftime("%d %B %Y %H:%M:%S.000") + "'"	

import sys, os, time

from optparse import OptionParser

parser = OptionParser()

# test and verbose flags
parser.add_option("-t", "--test", action="store_true", dest="test", help="execute script")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="print debug")

# environment switches
parser.add_option("-s", "--server", action="callback", callback=store_value, type="string", nargs=1, dest="server", help="specify server name")
parser.add_option("-d", "--database", action="callback", callback=store_value, type="string", nargs=1, dest="database", help="specific database name")
parser.add_option("-r", "--revision", action="callback", callback=store_value, type="string", nargs=1, dest="revision", help="specify database revision")
parser.add_option("-e", "--environment", action="callback", callback=store_value, type="string", nargs=1, dest="environment", help="specify environment variable to switch ")

(options, args) = parser.parse_args()

print options, args


if options.server:
	ServerName = options.server			
	
if options.database:
	Database = options.database

if options.revision :
	Revision = options.revision

print ("\n\tServerName [%s] Database [%s] Revision [%s] Username & Password [NT]\n") % (ServerName, Database, Revision)

if options.test :

	import win32com.client						
	connexion = win32com.client.gencache.EnsureDispatch('ADODB.Connection')			
	cstr = "Provider=SQLOLEDB.1;Data Source=" + ServerName
	cstr = cstr + ";Initial Catalog=" + Database + ";Integrated Security=SSPI;"
	connexion.Open(cstr)

	AD_OPEN_KEYSET = 1
	AD_LOCK_OPTIMISTIC = 3

	rs = win32com.client.Dispatch(r'ADODB.Recordset')
	rs.CursorLocation = 3 

	offset = 1			
	
	rs.Open("exec someStoredProcedure", connexion, AD_OPEN_KEYSET, AD_LOCK_OPTIMISTIC)

	# expand the recordset as list of tuples
	if not (rs.BOF or rs.EOF):				
		rows = zip(*rs.GetRows())
		for item in rows:
			print item[0], item[1], item[2], item[4]
			
	rs.Close()																	
	connexion.Close()
