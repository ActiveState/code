#automate a log grabber script with telnetlib and ftplib
# LOG_GRABBER is a shell script which will grab the logs from the production logs. 
# It may invoke other shell script, perl, shell, python etc to get its job done.
# A generic example: getAccountBalance, 500 
# this means getAccountBalance function takes about 500 ms to finish. 
# its end result is saved in LOG_OUT in any format you may import later for analysis.  

import telnetlib
from ftplib import FTP

# full path to them
LOG_GRABBER='/users/perfmon/grabLogs.sh'
LOG_OUT='logstats.txt'

prdLogBox='142.178.1.3'
uid = 'uid'
pwd = 'yourpassword'

# kick off the log grabber via telnet

tn = telnetlib.Telnet(prdLogBox)

tn.read_until("login: ")
tn.write(uid + "\n")

tn.read_until("Password:")
tn.write(pwd + "\n")

tn.write(LOG_GRABBER+"\n")

tn.write("exit\n")

tn.close()


# download the timing statistics to local via FTP 

ftp=FTP(prdLogBox)
ftp.login(uid,pwd)
#ftp.set_debuglevel(2)
logOut=open(LOG_OUT,'wb+')
ftp.retrbinary('RETR '+LOG_OUT, logOut.write)
ftp.quit()
logOut.close()
