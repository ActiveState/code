import socket
from ftplib import FTP
true, false = 1, 0

def isFTPSiteUp(site):
	try:
	        FTP(site).quit()
		
	except(socket.error):
		return false
	return true


def refineFTPList(list):
	new_list = []

	for site in list:
		if isFTPSiteUp(site):
			new_list.append(site)
	
	return new_list	
				
sites = ['ftp.cdrom.com', 'ftp.redhat.com', 'ftp.ska143blah.com']

working_sites = refineFTPList(sites)
print working_sites
