#!/usr/local/bin/python
import pat  # touch pat.py in the cwd and try to import the empty file under Linux
import string 
import os,sys

################## os.getcwd()##############
def get_path():
	PAT=str(pat).split()[3][1:-9] # PATH extracted..
	sig=None
	try:
	 sig=os.remove(PAT + 'pat.pyc')# get_rid...
	except OSError:
	 PAT=PAT +'/'
	 sig=os.remove(PAT + 'pat.pyc')# Fix for mutiple calls..  
	return PAT
###############################
LOCATE=get_path()
print LOCATE # 
print os.getcwd()+ '/' #

print sys.argv[0] #
