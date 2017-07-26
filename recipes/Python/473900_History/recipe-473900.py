#!/usr/bin/env python

#Configuration section

hist_file = '/home/your_user/.py_history'
max_size_bytes = 1000000
max_size_lines = 10000

#Code section, no need to modify this

import readline
import rlcompleter
import atexit
import sys
from os.path import getsize

def reset_file(size,max_size,reason):
        try:
                print "Resetting history file %s because it exceeded %s %s; it has %s.\n" % (hist_file,max_size,reason,size,)
                f = open(hist_file,'w')
                f.close()
        except IOError, e:
                print "Couldn't reset history file %s [%s].\n" % (hist_file,e,)

def safe_getsize(hist_file):
        try:
                size = getsize(hist_file)
        except OSError:
                size = 0
        return size

lines = 0
size = safe_getsize(hist_file)

if size > max_size_bytes:
        reset_file(size,max_size_bytes,"bytes")
else:
        try:
                readline.read_history_file(hist_file)
                lines = readline.get_current_history_length()
                if lines > max_size_lines:
                        try:
                                readline.clear_history()
                        except NameError, e:
                                print "readline.clear_history() not supported (%s), please delete history file %s by hand.\n" % (e,hist_file,)
                        reset_file(lines,max_size_lines,"lines")
        except IOError:
                try:
                        f = open(hist_file,'a')
                        f.close()
                except IOError:
                        print "The file %s can't be created, check your hist_file variable.\n" % hist_file

size = safe_getsize(hist_file)

print "Current history file (%s) size: %s bytes, %s lines.\n" % (hist_file,size,readline.get_current_history_length(),)

readline.parse_and_bind("tab: complete")

atexit.register(readline.write_history_file,hist_file)
