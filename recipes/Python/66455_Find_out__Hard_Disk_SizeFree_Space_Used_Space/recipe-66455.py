"""
Author : Ratnakar Malla
This module , does not take any i/p file. It first does a net view
command , and gets the list of computers in the domain. Connects
to each computer , performs size check and returns the size of the
harddisk. Please note that , the file and dir sizes are caluclated
in DOS. Windows performs a sort of approximation. So there will be
slight  variation in the amount of space reported by DOS and Windows.
If I am not wrong DOS gives u the best values.
 """
import win32net
import string
import fpformat
import os
import calendar

f=os.popen("net view")
for x in f.readlines():
    if x.startswith("\\"):
        compName=x.split()[0]
        string.replace(compName,"\\","  ")
        cName=string.strip(compName)
        print "Now working on : ",cName
        try:
            win32net.NetUseDel(None,'Z:',0)
            print "Z: Drive already exists, deleting ... "
        except:
            print "Starting .."
        server=cName+ '\\' + 'c$'
       
        try:
            win32net.NetUseAdd(None,1,{'remote': server,'local':'Z:'})
            yr,mon,day,hr,min,sec,jk1,jk2,jk3=calendar.localtime()
            print "Start Time : %s:%s:%s" % (hr,min,sec)
            print "Connected to Z: drive ..."
            myStr=os.popen("dir /s /-C z:\\").readlines()
            print "reading lines into mystr...."
            UsedSpace=fpformat.fix(long(string.split(myStr[-2])[2])/(1000000000.0),2)
            FreeSpace=fpformat.fix(long(string.split(myStr[-1])[2])/(1000000000.0),2)
            TotalSpace=fpformat.fix((float(UsedSpace)+float(FreeSpace)),2)
            print "Used Space:  %s GB" % UsedSpace
            print "Free Space: %s GB" % FreeSpace
            print "Total Space: %s GB" % TotalSpace
            win32net.NetUseDel(None,'Z:',0)
            yr1,mon1,day1,hr1,min1,sec1,jk4,jk5,jk6=calendar.localtime()
            print "End Time : %s:%s:%s" % (hr1,min1,sec1)
        except:
            print "Could not connect to computer %s" % server
fw.close()
