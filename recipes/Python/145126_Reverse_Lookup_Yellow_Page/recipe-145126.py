#!/usr/bin/env python
"""
Reverse Phone lookup
usage: ryp.py -s mail.your.com -e youremail@your.com -p 4162986294
It needs SMTP server, your email wishes to receive the response and of course the phone number  
author: Victor Yang
"""
import httplib
import sys,os
import smtplib
import MimeWriter,base64,StringIO
import getopt
import re 


# change this to 
WP_SERVER="www.whitepages.com"
WP_PATH='/find_person_results.pl?fid=p&ac=%s&p=%s' 

emailPattern=re.compile("^.+@.+\..{2,3}$")
phonePattern = re.compile(r"^\D*1?\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)")


class InvalidEmail(Exception): pass
class InvalidPhoneNumber(Exception): pass

def validateEmail(email):
    match=emailPattern.match(email)
    if not match:
	raise InvalidEmail,email

def validatePhone(phoneNumber):
    match = phonePattern.match(phoneNumber)
    if not match:
        raise InvalidPhoneNumber, phoneNumber

def lookup(phoneNumber):
    list=phonePattern.split(phoneNumber)
    conn=httplib.HTTPConnection(WP_SERVER)
    conn.request('GET',WP_PATH % (list[1],list[2]+list[3]))    
    response=conn.getresponse()
    data=response.read()
    conn.close()
    return data
	
def sendmail(phoneNumber,data,toaddr):
   smtpConn=smtplib.SMTP(smtp_server)
   #smtpConn.set_debuglevel(1)
   fromaddr='admin@webspherediy.com'
   #msg=("From: %s\r\nTo: %s\r\n\r\n" % (fromaddr,toaddr)) 
   msg=data
    
   msg=StringIO.StringIO()
   writer=MimeWriter.MimeWriter(msg)
   writer.addheader('MIME-Version', '1.0')
   writer.addheader('Subject','reverse phone lookup result for: '+phoneNumber)
   writer.startmultipartbody('mixed')
   part=writer.nextpart()
   body=part.startbody('text/html')
   body.write(data)
   writer.lastpart()
   smtpConn.sendmail(fromaddr,toaddr,msg.getvalue())
   smtpConn.quit() 

def usage_exit(progname, msg=None):
    if msg:
        print msg
        print
    print "usage: %s -s|--smtp mail.your.com -e|--email joe@yahoo.com -p|--phone 416-456-2345 " % progname
    sys.exit(2)
	
if __name__ == '__main__':
  
  # init
  smtp_server=None
  phone=None
  toaddr=None  
  progname = os.path.basename(sys.argv[0])

  # get the toaddr, phone,smtpserver from sys.argv
  try:
     opts, args = getopt.getopt(sys.argv[1:], 'he:p:s:', ['help', 'email=','phone=','smtp='])
     #print opts,args
     for opt, value in opts:
           if opt in ('-h','--help'):
                usage_exit(progname)
           if opt in ('-e','--email'):
                toaddr = value
	   if opt in ('-p','--phone'):
		phone=value
	   if opt in ('-s','--smtp'):
		smtp_server=value
  except getopt.error, e:
        usage_exit(progname, e)
	  
  # bail out if we don't have phone , toaddr,smtp
  (smtp_server==None and usage_exit(progname)) or (phone==None and usage_exit(progname)) or (toaddr==None and usage_exit(progname)) 
  
  
  try:
      #validate phone number
      validatePhone(phone)
      #validate toaddr 
      validateEmail(toaddr) 
      sendmail(phone,lookup(phone),toaddr)
      print 'email has been sent to '+toaddr
  except InvalidEmail,email:
	print 'Invalid Email Address:', email 
  except InvalidPhoneNumber,phoneNumber:
	print 'Invalid Phone Number:',phoneNumber 
  except:
       print 'Unexpected error:', sys.exc_info()[1]
       raise 
