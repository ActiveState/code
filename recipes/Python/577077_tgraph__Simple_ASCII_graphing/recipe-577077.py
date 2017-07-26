#!/usr/bin/env python
#Copyright 2005 Drew Gulino
##This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program; if not, write to the Free Software
##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys,os,getopt
from getopt import GetoptError

class Tgraph:

    def __init__(self,display_number,columns,symbol,threshold,maximum):
        self.maximum = maximum
        self.display_number = display_number
        self.columns = columns
        self.symbol = symbol
        self.threshold = threshold

    def __del__(self):
        reset = os.popen('tput sgr0').read()
        sys.stdout.write( reset )

    def graph(self,num,max_num):
        sys.stdout.softspace = 0
        if num > 0:
            scale = float(self.columns / max_num)
            characters = int(num*scale)
            for iter in (range(0,characters)):
#                sys.stdout.softspace = 0    #This removes extra spaces after print statements
#                print self.symbol,
                sys.stdout.write(self.symbol)
                sys.stdout.flush()
            if self.display_number:
                sys.stdout.write(str(num))
                sys.stdout.write("\n")
                sys.stdout.flush()
            else:
                sys.stdout.write("\n")
                sys.stdout.flush()
        else:
            if self.display_number:
                sys.stdout.write(str(num))
                sys.stdout.write("\n")
                sys.stdout.flush()

def usage(progname):
    print "Usage: " + progname
    version()
    print "[-h --help]"
    print "[-v --version]"
    print "[-n --no_number] Don't display number w/graph"
    print "[-c --columns=] Display columns(default = 72)"
    print "[-s --symbol=] Symbol to display(default = '*')"
    print "[-t --threshold=] Will color lines over this value"
    print "[-m --maximum=] Presets the scale for this maximum value(default = 0)"

def version():
    print "version: 1.1"

def main(argv, stdout, environ):
    #TODO: Auto detect number of columns in display
    progname = argv[0]
    symbol = "*"
    columns = int(os.popen('tput cols').read()) - 8
    #columns = 72
    number = 0
    display_number = 1
    threshold = 0
    maximum = 0

    bold = os.popen('tput bold').read()
    reset = os.popen('tput sgr0').read()
    dim = os.popen('tput setaf 0').read()
    red = os.popen('tput setaf 1').read()
    green = os.popen('tput setaf 2').read()
    yellow = os.popen('tput setaf 3').read()
    blue = os.popen('tput setaf 4').read()
    magenta = os.popen('tput setaf 5').read()
    try:
        arglist, args = getopt.getopt(argv[1:], "hvnc:s:t:m:", ["help", "version", "no_number","columns=", "symbol=", "threshold=", "maximum"])
    except GetoptError:
        print "Invalid Option!"
        usage(progname)
        return

    # Parse command line arguments
    for (field, val) in arglist:
        if field in ("-h", "--help"):
            usage(progname)
            return
        if field in ("-v", "--version"):
            version()
            return
        if field in ("-n", "--number"):
            display_number = 0
        if field in ("-c", "--columns"):
            columns = int(val)
        if field in ("-s", "--symbol"):
            symbol = val
        if field in ("-t", "--threshold"):
            threshold = val
        if field in ("-m", "--maximum"):
                maximum = val


    tgraph = Tgraph(display_number,columns,symbol,threshold,maximum)
    while 1:
        number = sys.stdin.readline()
        if not number: break
        number = float(number)
        if number > float(tgraph.maximum):
            tgraph.maximum = number
            sys.stdout.write( bold )
        else:
            sys.stdout.write( reset )
        if tgraph.threshold > 0:
            if number >= float(tgraph.threshold):
                sys.stdout.write( red )
            else:
                sys.stdout.write( reset )
        tgraph.graph(float(number),float(tgraph.maximum))

if __name__ == "__main__":
    main(sys.argv, sys.stdout, os.environ)
