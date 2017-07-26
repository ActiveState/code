#!/usr/bin/python
# Check which version and uptime on the clients 

import os
import sys
import ftplib

hosts = ["192.168.15.101",
         "172.16.104.19",
         "192.168.1.111",
         "192.168.1.112",
         "172.16.104.21",
         "192.168.1.113",
         "192.168.1.114",
         "192.168.15.100",
         "172.16.104.16",
         "192.168.1.115",
	 "192.168.1.116",
	 "10.11.3.130"]

## Download /etc/borderlineversion and print the content of it

def getversion(ftp):
    file = "borderlineversion"
    ftp.cwd("/etc")
    ftp.retrbinary("RETR " + file, open(file, "wb").write)
    file = open("borderlineversion")
    for line in file:
        print ("Version: " +line.strip())

## Download /proc/uptime and than parse out the time from it and convert it to
## float and dived with 3600

def getuptime(ftp):
    file = "uptime"
    ftp.cwd("/proc")
    ftp.retrbinary("RETR " + file, open(file, "wb").write)
    file = open("uptime")
    for line in file:
        time = line.split()[0]
        timefloat = float(time)
        uptime = timefloat / 3600
        print "Uptime: ", "%.2f" % uptime, "timmar\n"

## Loop through the list of hosts
for x in hosts:
    print "Hosts: ", x
    try:
        ftp = ftplib.FTP(x)
        ftp.login("****", "****")
    except ftplib.error_perm, e:
        print "Login failed %s" % e
        sys.exit()
    except socket.error, e:
        print "Connection failed %s" % e
        sys.exit()
    getversion(ftp)
    getuptime(ftp)

## clean up after all the work

    ftp.close()
    os.remove("borderlineversion")
    os.remove("uptime")
