#!/usr/bin/env python2.4
from subprocess import *
import os

class myDHCPip:
    ip = None

    def __init__(self, interface='wlan0'):
        if os.name == 'posix':
            self.cmd = "/sbin/ip -f inet addr"
            self.searchstr = 'global ' + interface
        elif os.name == 'nt':
            self.cmd = "c:\WINDOWS\system32\ipconfig.exe"
            self.searchstr = 'IP Address'
        self.search4ip()

    def getdata(self):
        """get data about dhcp ip"""

        p = Popen(self.cmd.split() ,stdout=PIPE)
        return p.communicate()[0]

    def search4ip(self):
        """parse data to get ip"""

        ipstr = [line.strip()
                for line in self.data.split('\n')
                if line.find(self.searchstr) >0 ][0]
        if os.name == 'nt':
            self.ip = ipstr.split(':')[1]
        elif os.name == 'posix':
            self.ip = ipstr.split()[1].split('/')[0]

    def getip(self):
        return self.ip

    ip = property(fget = getip)
    data = property(fget = getdata)

if __name__ == '__main__':
    print myDHCPip('eth1').ip
    #print myDHCPip('eth1').data
