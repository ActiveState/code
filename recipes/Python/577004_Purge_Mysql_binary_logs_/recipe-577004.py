#!/usr/bin/python
#Name: Umang Gopani
#Purpose: Purging Binary logs from Master DBs.
#Disclaimer:Obviously, you use this document at your own risk. I am not responsible for any damage or injury caused by your use of this document, or #caused by errors  and/or omissions in this document. If that's not acceptable to you, you may not use this document. By using this document you are #accepting this disclaimer.

# Before executing emerge -av mysql-python numeric  (on Gentoo)
# Before executing apt-get install python-mysqldb  and apt-get install python-numeric (on Ubuntu)

import sys
import string
import array
import commands         # API for running unix commands
import MySQLdb          # API for accessing to Mysql database
from Numeric import *

# Database credentials
user = 'username'
password = 'mypassword'
database = 'mysql'

# Function returning the hostnames of slaves connected to the master DB.
def slave_host():
        try:
                db = MySQLdb.connect (host = "localhost",
                                        user = user,
                                        passwd = password,
                                        db = database)
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
        cursor = db.cursor()
        cursor.execute("show processlist" )     # Get the output of show processlist to find the slave hostname.For connected slave one can find the command column as "Binlog Dump".
        numrows = int(cursor.rowcount)
        cntr = 0
        slave1 = list([0, 0, 0])                # Initialising the slave1 variable for stopring the hostnames for slaves.RIght now it is limited to 3 slaves.
        for x in range(0,numrows):
                result1 = cursor.fetchone()
                if result1[4] == "Binlog Dump":
                        if ':' in result1[2]:           # Output is seen in the form of hosname:port number.
                                sslave = string.split(result1[2],':')           # Seperating port number from hostname.
                                slave1[cntr] = sslave[0]
                        cntr = cntr + 1
                        return slave1                           # Returning the name of the slave hostnames.
                else:
                        return 0


# This section gives the output as the fullpath of the directory in which the bin-logs reside on the Master.The information is extraceted form the mysql config file.
ldir = "cat /etc/mysql/my.cnf|grep log-bin"
ldiro = commands.getoutput(ldir)
ldirop = ldiro.rsplit()
if '/' in ldirop[2]:            # Output of log-bin gives the full path name icluding the filename.
        ts = string.split(ldirop[2],'/')        # Seperating the filename, since it is not desired to check the disk space.
tsrem = ts[0:len(ts) -1]
jtsrem = string.join(tsrem,"/")         # Joining the string with "/" to give the full path of the directory.


# This section takes the full pathname form the previous section and checks the size of that partition using df -h
dfh = 'df -h %s' % jtsrem
dfho = commands.getoutput(dfh)
dfhop = dfho.rsplit()
dfhintop =  dfhop[11]           # Check the 11th variable in the array for percentage of size used.
num = dfhintop[0] + dfhintop[1]
if dfhintop[1] == "%":          # If the output is in 1 digit  i.e is less than 10%, then purgning is not required.
        print "Less than 10% of disk space being used.Aborting purgin of logs."
        sys.exit(0)
size = string.atoi(num)

# This section check for the latest master bin log file being used by the slave and gives it as the output.
if  slave_host() != 0:
        uhost = slave_host()            # Save the returned value  from the function slave_host into a variable.
#       print "Slave host name : %s" % uhost
        slvlog = list([0, 0, 0])
        for i in range(0,len(uhost)):
                if uhost[i] != 0:       # To keep a check on the number of slaves.If there is only 1 slave get the name and stop the loop.
                        rhost = uhost[i]
                        srhost = str(rhost)
                        try:
                                db = MySQLdb.connect (host="%s" % (srhost[0:]),
                                        user = user,
                                        passwd = password,
                                        db = database)
                        except MySQLdb.Error, e:
                                print "Error %d: %s" % (e.args[0], e.args[1])
                                sys.exit(1)
                        cursor = db.cursor()
                        cursor.execute("show slave status" )
                        result = cursor.fetchone()
                        slvlog[i] = result[9]
else:
        print "No slave connected to this master.Aborting purgin of logs.Will try again in next run."
        sys.exit(0)
flog = slvlog[i]        # Store the result into a variable. This is useful if there is only 1 slave to the master and the next loop is not followed.

# If the slaves are more than 1, compare which is the latest file being used by any slave.This is to avoid purgning a file being used by any other slave.
if i > 1:
        for x in range(0,i):
                if slvlog[x] != 0:
                        if slvlog[x] != slvlog[x+1]:
                                if slvlog[x] > slvlog[x+1]:
                                        flog = slvlog[x]
                                else:
                                        flog = slvlog[x+1]

final = str(flog)       # The final name of the file upto which teh logs needs to be purged have been stored in "final " variable.

# This is the section which will use the outputs form all the previous section and purge the binary logs if the disk space used is greater than 50%.
if size > 50:
        try:
                db = MySQLdb.connect (host="localhost",
                        user = user,
                        passwd = password,
                        db = database)
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
        cursor = db.cursor()
        sql = """ purge master logs to '%s' """ % (final[0:])   # Mysql command to purge binary logs from master.
#       print "Output is : %s" % sql
        cursor.execute(sql)
        print "Binary logs from master have been purged upto %s." % final
        sys.exit(0)
else:
        print "Less than 50% of disk space bein used.Aborting purging of logs."
        sys.exit(0)
