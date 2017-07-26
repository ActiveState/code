#! /usr/bin/env python
from optparse import OptionParser
import os,sys

doc=""" 
%prog [Options] [inputfile [outputfile]]
"""

#import re
#regexStr = ''
#regex = re.compile(regexStr)

lines = []

def processLine(line):
#    result = line.strip().split(':')
#     match = regex.match(line)
#    if match:
#        result = match.groups() 
    result = line.rstrip()
    lines.append(result)
    
def main():
    global options
    parser = OptionParser(version="%prog 0.0", usage=doc)
    parser.add_option("-o", "--logfile", dest="logfilename",
                      help="write log to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="print debug information")
    (options, args) = parser.parse_args()
    input = None    
    if len(args) <= 2:
        if len(args) > 0 and args[0] != '-':
            input = open(args[0], 'r')
    if not input:
       if options.debug: print >> sys.stderr, 'reading input from stdin'
       input = sys.stdin        
        
    if len(args) == 2: sys.stdout = open(args[1], 'w')

    if options.logfilename: options.logfile = open(options.logfilename, 'w')
    else:                   options.logfile = None

    if options.debug:
        print >> sys.stderr, "options:", options
        print >> sys.stderr, "args   :", args

#    lscmd = 'ls -lrt '
#    input = os.popen(lscmd).readlines()

    for line in input:
        processLine(line)
            
    for line in lines:
        if options.verbose:
            print line
    if options.verbose: print >> sys.stderr, '%d lines' % len(lines)
    if options.logfile: print >> options.logfile, '%d lines' % len(lines)
    sys.exit(0)
       
if __name__ == '__main__':
    main() 
