#! usr/bin/python

import dircache
import getpass
import time

logfile = open("spam.txt", "w+")

localtime = time.asctime( time.localtime(time.time()) )
print >> logfile, 'local current time :', localtime

usr = getpass.getuser()
print >> logfile, 'current user :' + usr

lst = dircache.listdir('/')
print >> logfile, lst

logfile.close()
