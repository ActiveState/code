'''
Created on feb 15, 2010

this IronPython script reads servers from a txt file C:\\servers.txt , connects to each server with the function RemoteConnect
Remoteconnect function reads the internal CPU TEMP from the WMI class MSAcpi_ThermalZoneTemperature located in namespace \root\WMI
if internal CPU temp exceeds a certian Threshold , the function sends an alerting e-mail , it can also send an alerting SMS using a modem (not included)
*settings crtcltemp depnds on your environmnet
*servers.txt contains a server name per line 
*Smtp server must support open relay from the sender ip address machine
@author: Mohamed Garrana
'''

import clr,time,os.smtplib  
clr.AddReference("System.Management")
from System.Management import  ManagementScope, ManagementObjectSearcher , WqlObjectQuery , ConnectionOptions


	
crtcltemp = 3000 # set the critical temprature here , converting from Celcuis to Tenth of kelvin , 15 c * 10 + 2732 = 2882   
	

#Remote connect function connects to a computer name with a username and password and reads "MSAcpi_ThermalZoneTemperature" from WMI
#if the Cpu temp exceeds a certian Threshold, an alerting e-mail is sent 	
def RemoteConnect(computername):
	options = ConnectionOptions()
	options.EnablePrivileges = True
	options.Username = "Administrator" #set your username here
	options.Password = "Password" #set your password here
	network_scope = r"\\%s\root\WMI" %computername
	print network_scope
	scope =  ManagementScope(network_scope, options)
	query = "Select * from  MSAcpi_ThermalZoneTemperature"
	searcher = ManagementObjectSearcher(scope, WqlObjectQuery(query), None)
	for cpu in searcher.Get():
		nowtemp = int(cpu["CurrentTemperature"])
		print nowtemp
		if nowtemp >= crtcltemp:
			print " critical temprature on %s" %(computername,)
			#command= "python c:\\alertsms.py %s" %(computername,) # calling another script with cpython for pyserial extension to work (alert by sms)
			sender = 'SpiderAlert@sendermail.com'  #set the sender e-mail address
			receivers = ['Admin@tomail.com']	#set the receiver e-mail address
			# setting the e-mail Message (from,to,Subject,body)
			message = """From: From Person <SpiderAlert@sendermail.com> 
			To: To Person <'Admin@tomail.com'>
			Subject: Spider Temperature Control Alerting System

			Temparature is critical on server %s .
			""" %computername
			#trying to send an e-mail
			try :
				mailobj=smtplib.SMTP("mailserver") #set the ip address of the SMTP mail server supporting open relay
				mailobj.sendmail(sender, receivers, message)         
				print "Alert E-mail sent Successfully "
			except :
				print "Error: unable to send Alert using e-mail"
			
			print command
			os.popen(command)
		
		else:
			print "Temperature normal on %s" %(computername,)	


#opening a txt file with server names to monitor			
fo=open('c:\\servers.txt','r')
listofservers=fo.readlines()
numberofservers=len(listofservers)
j=0

#infinite loop going through the servers one by one to the RemoteConnect function
while 1:
	server = listofservers[j].strip()
	print server
	RemoteConnect(server)
	time.sleep(60)
	j=j+1
	if  j == numberofservers: 
		j=0
	else:
		continue
