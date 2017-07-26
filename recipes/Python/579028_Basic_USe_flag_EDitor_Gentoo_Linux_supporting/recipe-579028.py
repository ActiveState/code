#!/usr/bin/env python

import os
import re
import sys
import string
import subprocess

class Abused:

    def __init__(self, args):
        if args:
            self.args = ' '.join(args)
        else:
            self.args = ''
            
        self.pcmd     = 'emerge -pv --color y'
        self.rcmd     = 'emerge -v --quiet-build --color y'
        self.flags_d  = []
        self.flags_c  = []
        self.pkglines = []
        
        # pretend so we can see the use flags
        print 'Examining USE flags...'
        self.__getUse()

        # display the current USE flags, and allow some editin
        while not self.__editor():
            pass

        # and fire off the real emerge
        self.__doEmerge()

    def __sanitize(self, data):
        retv = ''
        if data.find('\x1b') != -1:
            tmp = filter(lambda x: x in string.printable, data)
            retv += re.sub('(\{|\})', '', re.sub('\[[0-9\;]+m', '', tmp))
            return retv
        return False
    
    def __getUse(self):        
        cmd_s = 'USE="%s" %s %s' % (
            ' '.join(self.flags_c),
            self.pcmd,
            self.args
        )
        cmd_p = subprocess.Popen(
            cmd_s,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash"
        )

        self.pkglines  = []
        self.flags_d   = []
        self.flags_c   = []
        self.longest_c = ''
        self.longest_n = 0
        
        buff = cmd_p.stdout.readline()
        while buff:
            if buff.strip().find('USE="') != -1:
                self.pkglines.append(buff.strip())
                flags_t = buff.strip().split('USE="')[1].split('"')[0].split()
                for f in flags_t:
                    if f not in self.flags_d:
                        self.flags_d.append(f)
                        if len(f) > self.longest_n:
                            self.longest_n = len(f)
                            self.longest_c = f
            buff = cmd_p.stdout.readline()

        # And build our sanitized list of use flags
        for f in self.flags_d:
            t = self.__sanitize(f)
            self.flags_c.append(t)

    def __editor(self):
        print
        for l in self.pkglines:
            print l
        print
        a = 0
        for i in self.flags_d:
            eval("sys.stdout.write('%%%ds' %% i)" % (self.longest_n+1))
            if a < 4:
                a += 1
            else:
                print
                a = 0

        sys.stdout.write("\n\n")
        sys.stdout.write('>> ')
        sys.stdout.flush()
        
        data = sys.stdin.readline().strip().split()        
        if len(data) == 0:
            return True
        else:
            # go through and replace the flags that are edited
            for f in data:
                for ix in range(0, len(self.flags_c)):
                    if self.flags_c[ix].find(f[1:]) != -1:
                        if f[0] == '-' and self.flags_c[ix][0] != '-':
                            tt = self.flags_c[ix]
                            self.flags_c[ix] = '-%s' % tt
                        elif f[0] != '-' and self.flags_c[ix][0] == '-':
                            tt = self.flags_c[ix][1:]
                            self.flags_c[ix] = tt
            # then refresh the data
            self.__getUse()
            return False

    def __doEmerge(self):
        cmd_s = 'USE="%s" %s %s' % (
            ' '.join(self.flags_c),
            self.rcmd,
            self.args
        )
        cmd_p = subprocess.Popen(
            cmd_s,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            executable="/bin/bash"
        )
        buff = cmd_p.stdout.readline()
        while buff:
            sys.stdout.write(buff)
            sys.stdout.flush()
            buff = cmd_p.stdout.readline()
    
if __name__ == '__main__':
    try:
        app = Abused(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)
