#!/usr/bin/python

import re

class WinIni:
 """
 Read information from a text file formatted in WIN.INI format.
 """
 def __init__(self, filename):
   self.__hash = {}
   sec = re.compile(r'^\[(.*)\]')
   eq = re.compile(r'^([^=]+)=(.*)')
   for line in open(filename, "r").readlines():
      if sec.search(line): 
         lbracket, section, rbracket = sec.split(line)
         section = section.strip() # remove leading and trailing spaces
      elif eq.search(line):
         left, item, value, right = eq.split(line) 		
         self.__hash[section+'.'+item.strip()] = value.strip()
				
 def __getitem__(self, aItem):
   return self.__hash[aItem]
