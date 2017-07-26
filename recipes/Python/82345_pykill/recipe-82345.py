#!/usr/bin/env python
import commands
import os,sys,string
import re

def pkill():
    if len(sys.argv) <= 1:
        print "usage: " + sys.argv[0] + " process_name"
        sys.exit(1)
    rip = sys.argv[1]
    me = commands.getoutput("whoami")
    p = commands.getoutput("ps -u %s -o fname -o pid" % me)
    
    ids = p.split("\n")
    for id in ids:
        if id.find(rip) < 0:
            continue
        regex = re.compile(r'(\d+).*',re.I)
        id = regex.sub(r'\1', id)
        print "killing: %s\n" % id
        commands.getoutput("kill -15 %s" % id)
        if commands.getoutput("ps -u %s -o fname -o pid" % me).find(id) > -1:
            print "slaughtering: %s\n" % id
            commands.getoutput("kill -9 %s" % id)
if __name__ == '__main__' :
    pkill()
