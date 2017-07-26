#!/usr/bin/env python
"""
A simple script for making random passwords, WITHOUT 1,l,O,0.  Because
those characters are hard to tell the difference between in some fonts.

"""

#Import Modules
import sys
from random import Random

rng = Random()

righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
lefthand = '789yuiophjknmYUIPHJKLNM'
allchars = righthand + lefthand

try:
 passwordLength = int(sys.argv[1])
except:
 #user didn't specify a length.  that's ok, just use 8
 passwordLength = 8
try:
 alternate_hands = sys.argv[2] == 'alt'
 if not alternate_hands:
  print "USAGE:"
  print sys.argv[0], "[length of password]",
  print "[alt (if you want the password to alternate hands]"
except:
 alternate_hands = False

for i in range(passwordLength):
 if not alternate_hands:
  sys.stdout.write( rng.choice(allchars) )
 else:
  if i%2:
   sys.stdout.write( rng.choice(lefthand) )
  else:
   sys.stdout.write( rng.choice(righthand) )
