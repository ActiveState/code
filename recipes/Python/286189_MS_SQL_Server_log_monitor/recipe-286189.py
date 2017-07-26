# sqlaerrorlog.py - M.Keranen (mksql@yahoo.com) [06/23/2004]
# ------------------------------------------------------------------------------------------------
# A script to gather error and warning information from MS SQL Server and SQL Server Agent logs,
# from multiple servers, and create a single report in HTML. Currently looks for Errors, Warnings,
# and failed Agent jobs. Used as a start of day / quick check to determine if any servers need
# attention from an administrator.
#
# Can authenticate using wither native SQL logins, or a Windows Domain login. Server names and
# authentication method stored in a text config file.
# -------------------------------------------------------------------------------------------------
# Usage: drivespace.py drive_list_cfg_file | *  (* = prompt for external domain user ID)

import getpass,string,sys,win32com.client
from win32com.client import DispatchBaseClass

cfgfile=sys.path[0]+'/sqlaerrorlog.cfg'

print
pw = getpass.getpass()
uid = getpass.getuser()

htmfile = open('C:\\Documents and Settings\\All Users\\DESKTOP\\Logs\\SQLErrorLog.htm','w')

htmfile.write('<TITLE>SQL Server Error Logs</TITLE>\n')

for line in open(cfgfile,'r').readlines():
	if line[0]<>'#':
		servers = string.split(string.strip(line),',')
		svr=servers[0]
		auth=servers[1]

		print '%s (%s)' % (svr,auth)

		htmfile.write('<TABLE WIDTH=100% CELLPADDING=2 BORDER=2>\n')

		htmfile.write('<TR>\n')
		htmfile.write('<TD BGCOLOR=#D4D4D4 ALIGN=CENTER VALIGN=top WIDTH=10%><B><FONT FACE="ARIAL" SIZE=2>' + svr + '</FONT></B></TD>\n')
		htmfile.write('<TD BGCOLOR=#D4D4D4 ALIGN=CENTER VALIGN=top WIDTH=90%><B><FONT FACE="ARIAL" SIZE=2>SQL Log Entry</FONT></B></TD>\n')
		htmfile.write('</TR>\n')

		sql = win32com.client.Dispatch('SQLDMO.SQLServer')
		
		if auth == 'S':
			sql.LoginSecure = 0
			sql.Connect(svr,uid,pw)
		else:
			sql.LoginSecure = 1
			sql.Connect(svr)
				  
		log = sql.ReadErrorLog()
		for r in range(1,log.Rows):
			lrow = log.GetColumnString(r,1)
			lurow = string.upper(lrow)
			if (('ERROR:' in lurow) and not ('0 ERRORS' in lurow)) or ('FAIL' in lurow) or ('WARN' in lurow):
				while r<log.Rows and log.GetColumnLong(r+1,2) > 0:
					r += 1
					lrow = lrow + log.GetColumnString(r,1)               
				htmfile.write('<TR>\n')
				htmfile.write('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (svr))
				htmfile.write('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (lrow))
				htmfile.write('</TR>\n')
		sql = None

		htmfile.write('<TR>\n')
		htmfile.write('<TD BGCOLOR=#E4E4E4 ALIGN=CENTER VALIGN=top WIDTH=10%><B><FONT FACE="ARIAL" SIZE=2>' + svr + '</FONT></B></TD>\n')
		htmfile.write('<TD BGCOLOR=#E4E4E4 ALIGN=CENTER VALIGN=top WIDTH=90%><B><FONT FACE="ARIAL" SIZE=2>Agent Log Entry</FONT></B></TD>\n')
		htmfile.write('</TR>\n')

		adoConn = win32com.client.Dispatch('ADODB.Connection')

		if auth == 'S':
			connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=msdb;User ID=%s;Password=%s;" % (svr,uid,pw)
		else:
			connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=msdb;Integrated Security=SSPI;" % (svr)

		sql = '''
		SELECT sysjobs.name, 
			hist.message + '(' + CAST(hist.run_date as varchar) + '-' + CAST(hist.run_time as varchar) + ')' as message
			FROM sysjobs, sysjobhistory as hist
			WHERE sysjobs.job_id = hist.job_id
				AND hist.run_status = 0
				AND hist.instance_id = (SELECT MAX(instance_id) FROM sysjobhistory WHERE sysjobhistory.job_id = sysjobs.job_id)
		'''

		adoConn.Open(connect)
		alog = adoConn.Execute(sql)

		while not alog[0].EOF:
			task=alog[0].Fields(0).Value
			entry=alog[0].Fields(1).Value
			htmfile.write('<TR>\n')
			htmfile.write('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (task))
			htmfile.write('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (entry))
			htmfile.write('</TR>\n')
			alog[0].MoveNext()
		
		htmfile.write('</TABLE>\n')

htmfile.close()
adoConn = None

xit = raw_input('\nPress Enter...')

"""
Example of sqlaerrorlog.cfg file:

#server_name, S/W = SQL / Windows Authentication
#-----------------------------------------------
SQLSERVER1,S
SQLSERVER2,W

"""
