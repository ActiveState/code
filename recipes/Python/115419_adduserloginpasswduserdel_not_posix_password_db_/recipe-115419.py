# These are multiple .py files that can be used
# to access the password file.
# adduser.py adds a login/password to the database
# login.py attempts to login using a supplied l/p
# passwd.py allows the user to change his password
# userdel.py allows user to delete him/her self
#
# #----cut here----# is where the file ends

# adduser.py
#
# Copyright (c) 2001 Nelson Rush. All rights reserved.
#
# add user to the password database
#
from os import *
from struct import *
from binascii import *
from getpass import *
from strop import *
import md5
import sys
if access("passwords",O_RDWR):
    fd = open("passwords",O_BINARY|O_RDWR)
    newfile = 0
else:
    fd = open("passwords",O_BINARY|O_RDWR|O_CREAT)
    newfile = 1
md5sum = md5.new()
fmt = "40s 256s 30s 32s h"
print "Please enter the following information to add a user:\n\n"
user_name = raw_input("name: ")
user_home = raw_input("home: ")
user_login = raw_input("login: ")
user_password = getpass("password: ")
md5sum.update(user_password)
user_passhash = hexlify(md5sum.digest())
user_attempts = 0
user_sizeof = calcsize(fmt)
user_info = pack(fmt,user_name,user_home,user_login,user_passhash,user_attempts)
user_data = user_info
if newfile:
    print "Adding user. . ."
    write(fd,user_info)
    close(fd)
    sys.exit(1)
while len(user_data) == user_sizeof:
    user_data = read(fd,user_sizeof)
    if len(user_data) == user_sizeof:
        (u_name,u_home,u_login,u_passhash,u_attempts) = unpack(fmt,user_data)
        if find(u_login,user_login) == 0:
            print "User already exists in database."
            close(fd)
            sys.exit(-1)
print "Adding user. . ."
write(fd,user_info)
close(fd)

#----cut here----#

# login.py
#
# Copyright (c) 2001 Nelson Rush. All rights reserved.
#
# login system which takes l/p and verifies access
#
from os import *
from struct import *
from binascii import *
from strop import *
from getpass import *
import md5
import sys
if access("passwords",O_RDONLY):
    fd = open("passwords",O_BINARY|O_RDONLY)
else:
    print "No password database exists."
    sys.exit(-1)
md5sum = md5.new()
fmt = "40s 256s 30s 32s h"
user_name = "Nothing"
user_home = "Nothing"
user_login = raw_input("login: ")
user_password = getpass("password: ")
md5sum.update(user_password)
user_passhash = hexlify(md5sum.digest())
user_attempts = 0
user_sizeof = calcsize(fmt)
user_data = pack(fmt,user_name,user_home,user_login,user_passhash,user_attempts)
while len(user_data) == user_sizeof:
    user_data = read(fd,user_sizeof)
    if len(user_data) == user_sizeof:
        (u_name,u_home,u_login,u_passhash,u_attempts) = unpack(fmt,user_data)
        if find(u_login,user_login) == 0 and u_passhash == user_passhash:
            print "Access Granted!"
            close(fd)
            sys.exit(1)
print "Invalid login or password."
close(fd)
sys.exit(-1)

#----cut here----#

# passwd.py
#
# Copyright (c) 2001 Nelson Rush. All rights reserved.
#
# changes a password
#
SEEK_BEG = 0
SEEK_CUR = 1
SEEK_END = 2
from os import *
from struct import *
from binascii import *
from strop import *
from getpass import *
import md5
import sys
if access("passwords",O_RDWR):
    fd = open("passwords",O_BINARY|O_RDWR)
else:
    print "No password database exists."
    sys.exit(-1)
md5sum = md5.new()
fmt = "40s 256s 30s 32s h"
user_name = "Nothing"
user_home = "Nothing"
user_login = raw_input("login: ")
user_password = getpass("OLD password: ")
md5sum.update(user_password)
user_passhash = hexlify(md5sum.digest())
user_attempts = 0
user_sizeof = calcsize(fmt)
user_data = pack(fmt,user_name,user_home,user_login,user_passhash,user_attempts)
while len(user_data) == user_sizeof:
    user_data = read(fd,user_sizeof)
    if len(user_data) == user_sizeof:
        (u_name,u_home,u_login,u_passhash,u_attempts) = unpack(fmt,user_data)
        if find(u_login,user_login) == 0 and u_passhash == user_passhash:
            new_password = getpass("NEW password: ")
            newmd5sum = md5.new(new_password)
            new_passhash = hexlify(newmd5sum.digest())
            user_info = pack(fmt,u_name,u_home,u_login,new_passhash,u_attempts)
            lseek(fd,-user_sizeof,SEEK_CUR)
            write(fd,user_info)
            close(fd)
            print "Password changed."
            sys.exit(1)
print "Invalid login or password."
close(fd)
sys.exit(-1)

#----cut here----#

# userdel.py
#
# Copyright (c) 2001 Nelson Rush. All rights reserved.
#
# deletes a user in the password database
#
SEEK_BEG = 0
SEEK_CUR = 1
SEEK_END = 2
import os
from struct import *
from binascii import *
from strop import *
from getpass import *
import md5
import sys
if os.access("passwords",os.O_RDWR):
    fd = os.open("passwords",os.O_BINARY|os.O_RDWR)
else:
    print "No password database exists."
    sys.exit(-1)
md5sum = md5.new()
fmt = "40s 256s 30s 32s h"
(fmode, fino, fdev, fnlink, fuid, fgid, fsize, fatime, fmtime, fctime) = os.fstat(fd)
user_name = "Nothing"
user_home = "Nothing"
user_login = raw_input("login: ")
user_password = getpass("password: ")
md5sum.update(user_password)
user_passhash = hexlify(md5sum.digest())
user_attempts = 0
user_sizeof = calcsize(fmt)
user_data = pack(fmt,user_name,user_home,user_login,user_passhash,user_attempts)
while len(user_data) == user_sizeof:
    user_data = os.read(fd,user_sizeof)
    if len(user_data) == user_sizeof:
        (u_name,u_home,u_login,u_passhash,u_attempts) = unpack(fmt,user_data)
        if find(u_login,user_login) == 0 and u_passhash == user_passhash:
            curpos = os.lseek(fd,0,SEEK_CUR)
            if curpos == fsize:
                os.close(fd)
                f = open("passwords","ab+")
                f.truncate(fsize - user_sizeof)
                f.close()
                print "User deleted."
                sys.exit(1)
            buf = os.read(fd,fsize - curpos)
            os.lseek(fd,curpos - user_sizeof,SEEK_BEG)
            os.write(fd,buf)
            os.close(fd)
            f = open("passwords","ab+")
            f.truncate(fsize - user_sizeof)
            f.close()
            print "User deleted."
            sys.exit(1)
print "Invalid login or password."
os.close(fd)
sys.exit(-1)
