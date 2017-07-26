# drivespace.py - M.Keranen (mksql@yahoo.com) [10/05/2004]
# -------------------------------------------------------------
# Reads a file containing a list of share names,
# and prints a report of the current free space on the volumes. 
# -------------------------------------------------------------

import getpass,os,string, sys
import win32file, win32net, win32wnet, win32netcon

cfgfile=sys.path[0]+'/drivespace2.cfg'
cfglines = open(cfgfile,'r').readlines()
cfglines.sort()

# Compile a list of domains in the config file
domains = []
for line in cfglines:
	target = string.split(string.strip(line),'\\')
	if len(target)>2 and target[0] not in domains: domains.append(target[0])	

# Create a dict of domain\user_id:password
domid ={}
#domid['(local)']=getpass.getuser(),getpass.getpass()
for domain in domains:
	string.strip(domain)
	uid = string.strip(raw_input('UserID for %s: ' % domain))
	if uid != '':
		pw = string.strip(getpass.getpass())
		domid[domain] = domain+'\\'+uid,pw
	else: domid[domain] = '',''
	print

lastserv = ""
xit = " "
while xit == " ":
	print "\n%s \t %s \t %s\t%s" % ("Server\share","%Free","Avail MB","Total MB")
	print   "%s \t %s \t %s\t%s" % ("------------","-----","--------","--------")
	for line in cfglines:
		if line[0]<>'#':
			line = string.strip(line)
			target = string.split(line,'\\')
	
			if len(target)==2:
				server = '\\\\'+target[0]
				share = '\\\\'+line
				uid = getpass.getuser()
				pw = None
			elif len(target)==3:
				domain = target[0]
				server = '\\\\'+target[1]
				share = '\\\\'+target[1]+'\\'+target[2]
				uid = domid[domain][0]
				pw = domid[domain][1]

			if server != lastserv and lastserv != "":
				try: win32wnet.WNetCancelConnection2(lastserv, 0, 0)
				except: warn = "!"
			if server != lastserv and uid != '':
				try: win32wnet.WNetAddConnection2(win32netcon.RESOURCETYPE_DISK, None, server, None, uid, pw, 0)
				except: print "%s\t  (WNetAddConnection2 failed [%s])" % (server,uid)
				lastserv = server

			fs,ts,fp = 0,0,0

			if uid != '':
				try: space = win32file.GetDiskFreeSpaceEx(share)
				except:
					warn = " "
					fp = "(GetDiskFreeSpaceEx failed)"
					fs,ts = '',''
				else:
					fs = int(space[0]/1048576)
					ts = int(space[1]/1048576)
					fp = int((float(space[0])/float(space[1]))*100)
					if fp<16: warn = "!"
					else: warn = " "

				print "%s \t %s%s \t %s\t\t%s" % (share[2:],warn,fp,fs,ts)
	
	try: win32wnet.WNetCancelConnection2(lastserv, 0, 0)
	except: warn = "!"
	xit = raw_input('\nPress Enter to exit (Space, Enter to rerun)...')

"""
Example of drivespace.cfg file:
-------------------------------
local1\c$
domain2\remote2\c$
"""
