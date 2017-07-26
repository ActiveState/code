'****************************************************'
'Created by C. Nichols #B0)~                         '
'E-mail: oldnich@digitaldarknet.net                  '
'Created: 11/16/02                                   '
'Updated! 11/19/02                                   '
'Version: Python 2+                                  '
'Desc: IPy Notify for Micro$oft Windoze              '
'Use: To notify whomever that your IP address has    '
'changed if you have a non-static IP address and run '
'a web server, game server, etc.                     '
'****************************************************'
'                                                    '
'                                                    '
'                        #                           '
'                       0 0                          '
'~~~~~~~~~~~~~~~~~uuu~~~~U~~~~uuu~~~~~~~~~~~~~~~~~~~~'
"!!!!!!!!!!!!HERE'S LOOKING AT YOU KID!!!!!!!!!!!!!!!"
'****************************************************'
import os, os.path, string, time
import smtplib, socket
import win32api
# GLOBALS --------------------------------------------
(head,tail) = os.path.split(win32api.GetSystemDirectory()) # Get the win path.
(ldrive,os_root) = os.path.split(head) # Now get the local drive.

# The path will generally, if not always be c:\
# Path_log = ldrive+'\yourdir\IPy_Notify.log'
# will specify a dir of your choice - dir must be created.
Path_dat = ldrive+'IPy_Notify.dat' # Program requires this file to run properly.
Path_log = ldrive+'IPy_Notify.log'

Name = win32api.GetComputerName() # Get actual machine name.

#Add your server name, mail server, and email addresses receiving notification.
MailServer = 'smtp.yourprovider.com'
Address    = ['yourmail@yourprovider.com']
#Address    = ['yourmail@yourprovider.com','yourfriend@something.com'] # Multiple Addresses - uncomment will override above.
Frm_add    = 'yourmail@yourprovider.com' # From must be a valid e-mail address or the mail function will fail.

# If your ISP requires authentication, leave blank if unsure and test.
User       = ''
Pass       = ''

# Functions ------------------------------------------

def mail(to='',frm='',subj='',body='',server=''):
    try:
        message='From: %s\r\nTo: %s\r\nSubject: %s\r\n%s'%(frm,to,subj,body)            
        mail=smtplib.SMTP(server)
        mail.sendmail(frm,to,message)
        mail.close()
    except:
        try:
            # Logon to the server... If needed
            message='From: %s\r\nTo: %s\r\nSubject: %s\r\n%s'%(frm,to,subj,body)            
            mail=smtplib.SMTP(server)
            mail.login(User,Pass) 
            mail.sendmail(frm,to,message)
            mail.close()
        except:
            print 'ERROR: Unable to send notification! - '+time.ctime()
            open(Path_log,'a').write(time.ctime()+' \nERROR: Unable to send notification!')

def start():
    def getIP(name, path):
        print 'IPy Notify by C. Nichols, 2002.\n'
        ip = socket.gethostbyname(name)
        print 'Current ip: '+str(ip)
        open(path,'w').write(ip) #Save the current IP address.
        out(name,Path_dat)

    def out(name, path, stat=1):
        while stat:
            cur_ip = open(path,'r').readline()
            new_ip = str(socket.gethostbyname(name))
            if cur_ip==new_ip:
                print 'Sleeping...'
                time.sleep(15) # Sleep in seconds - adjust polling interval to your taste.
                print 'Polling: '+new_ip+', '+time.ctime()
            else:
                print 'IP address has changed: '+new_ip
                open(Path_log,'a').write(time.ctime()+'\nINFO: IP address has changed: '+new_ip)

                print 'sending notification...'
                for add in Address:
                    mail(to=add,frm=Frm_add,subj='Message from '+name,body='New IP address: '+new_ip+' assigned to '+name, server=MailServer)
                getIP(name,Path_dat) 
                stat=0

    getIP(Name,Path_dat)
    
# Run ------------------------------------------------
# Make sure this is started via the command line or
# by a .cmd file in startup - The command window can
# be hidden from a cmd file if you hate it like I do.
# Download Python @ www.python.org or PythonWin
# (active python) from www.activestate.com.
try:
    open(Path_log,'a').write(time.ctime()+' START: IP Polling\n------------------------------------------\n')
    start()
except:
    open(Path_log,'a').write(time.ctime()+' \nERROR: IPy Notify failed!')
