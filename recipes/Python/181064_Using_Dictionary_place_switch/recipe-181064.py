#! /usr/local/bin/python

# /////////////////////////////////////////////////////////////////////////
# /**
# * Title: rochambeau.py
# *
# * Description: Rock, Scissors, Paper Game. 
# *              Shows a clean way of implementing a 'switch'
# *              statement in Python via a dictionary container. 
# *              The dictionary is made up of known 'named states' that
# *              are tested in sequence for their current 'state'.
# *
# * Copyright: Copyright (c) 2003
# *            This file is distributed as EXAMPLE SOURCE CODE ONLY!
# *            The following code is considered 'Freeware' and can be 
# *            freely copied/reused/distributed as needed. 
# *
# * Company: None
# * @author: Alan Haffner
# * @version 1.0
# */
# 
# /////////////////////////////////////////////////////////////////////////
# Date: 02/16/03


import os, sys
import string, random
import types

def cli():

   c = '?'
   while c not in 'rps':

      try:
         print
         # tailing index '[0]' picks only first char from input
         c = raw_input('\tPlease enter (r)ock, (p)aper or (s)cissors to play... ')[0]
      except IndexError:
         # bad input, so like get another...
         pass

      c = c.lower()

      #   x, q...   --> quit
      if c in ('x', 'q' ):
         raise 'USER_QUIT_ERROR'

   return c

if __name__=='__main__':

   errorCode = 0

   stateList = ['r', 'p', 's']

   validStates = { 'User Wins'      : (('p','r'), ('r','s'), ('s','p')),
                   'No One Wins'    : (('p','p'), ('r','r'), ('s','s')),
                   'Computer Wins'  : (('r','p'), ('s','r'), ('p','s')),
   }

   try:
      while 1:
         testTuple     = (None, None)
         userInput     =        None
         computerInput =       '?'

         userInput     = cli()
         computerInput = ( stateList[random.randint(0,2)] )
   
         testTuple = (userInput, computerInput)

         for select in validStates:
            if testTuple in validStates[select]:
               print
               print "You chose:         ", userInput
               print "The computer chose:", computerInput
               print " ****", select, " ****" 
               print

   # Note: By convention, all local exception 'constants' end 
   # in '_ERROR' regaurdless of their intended use. 
   except KeyboardInterrupt:
      print '\n' * 3
      print '[interrupted by user]'
      print '\n' * 3
   except 'USER_QUIT_ERROR':
      print '\n' * 3
      print '[interrupted by user]'
      print '\n' * 3
   except:
      # unexpected error
      print '\n' * 3
      traceback.print_exc()
      print '\n' * 3

      errorCode = 2

   sys.exit(errorCode)
