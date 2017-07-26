#!/usr/bin/env python
# Eli Criffield <python@zendo.net>
# avalible at http://eli.criffield.net/sum/
# a better better command line calculator,
#
# put this in a file, run it, cut and past a bunch of numbers (don't
# worry about the $ signs and commas) hit enter and it adds them up
# use / * -  + like normal
#
# added features over just using python as a command line calculator
# * numbers can include ,s and $s or anything really and it still works
#   this allows you to cut and paste things like $1,123.65 and it still works
# * add by default! (unless you run with -x)
#   cut and paste a bunch of numbers hit enter and it'll add them all up
# * command line history and readline, up arrow recalls your history
#   even between sessions
# * _ is the last answer, just like in python

import readline
import re
import os
import sys
import atexit

histfile = os.path.join(os.environ["HOME"], ".sumhist")
try:
    readline.read_history_file(histfile)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)

# if ran with -x don't add by default
if len(sys.argv) > 1:
   if sys.argv[1] == "-x":
      nodefsum = True
   else:
      nodefsum = False
else:
   nodefsum = False

del os, atexit, readline, sys, histfile

while 1 :
   try:
      __equation = raw_input("> ")
   except EOFError:
       break
   # substitue out anything not equation like
   __equation = re.sub('([a-zA-Z]|\,|\$|\`|\!|\@|\#|\$|\&|\{|\}|\[|\]|\~|\?|\<|\>|\|)',"",__equation)

   if nodefsum:
      __equation = re.sub('(\s+)'," ",__equation)
   else:
      __equation = re.sub('(\s+)',"+",__equation)
      __equation = re.sub('\+$',"",__equation)

   try:
      _ = eval(__equation)
   except:
      print "ERROR:%s"%__equation
   else:
      print _
