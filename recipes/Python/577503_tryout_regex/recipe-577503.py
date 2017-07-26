#!/usr/bin/python

#
# tests regex with matches
# handy utility to learn regex in python

#(c)lostp, 2010 December

#version 0.0.1

import re

class AppModel:
  pass

AppModel.regexstr = ''
AppModel.matchstr = ''

def main():
    while(1):
        line = raw_input("REGEX>")
        l = line.split()
        if (line[:7] == 'compile'):
            try:
                AppModel.regexstr = l[1]
                AppModel.compiledobj = re.compile(AppModel.regexstr)
            except:
                print "%s is not a valid regex" % AppModel.regexstr
                continue
        else:
            AppModel.matchstr = line
            matches()

def matches():
    if AppModel.compiledobj.match(AppModel.matchstr):
        print "%s matches the pattern %s" % (AppModel.matchstr,AppModel.regexstr)
    else:
        print "%s does not match the pattern %s" % (AppModel.matchstr,AppModel.regexstr)

if __name__ == '__main__':
    main()
