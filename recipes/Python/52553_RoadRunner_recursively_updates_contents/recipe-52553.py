#!/usr/bin/env python 

# $Id. RoadRunner.py Thu Apr 5 10:49:48 EST 2001 JuanCarlos.Leon $   

import os 
import string 
import re 
import sys 

_files_lst=[]  

def pluggit(readlines,regx,addstrng): 
	""" Append a string to desire regex pattern """ 
	lst=readlines 
	cregex=re.compile(regx)  
	for eachLine in lst: 
		match=cregex.search(eachLine)
		if match:
			rplacement=match.group()+addstrng
			f=re.sub(regx,rplacement,eachLine)  
			lindex=lst.index(eachLine) 
			lst.remove(eachLine)
			lst.insert(lindex,f) 
	return lst   

def compose(strng,regx,listoffiles=[]): 
	log=open('log.txt','w')  
	for xfile in listoffiles: 
		# Open file for read  
		readlines=open(xfile,'r').readlines()
		buffer=pluggit(readlines,regx,strng) 
		# We are good too open the file for writting  
		write_file=open(xfile,'w') 
		# Stuffed all buffer lines back to the original file  
		for line in buffer: 
			write_file.write(line)
		write_file.close()
		log.write('file %s updated\n' % (xfile)) 
	log.close()  


def fetch(path=None,ext='.html'): 
	if not path: 
		path=os.getcwd()  
	if os.path.isdir(path): 
		lst = os.listdir(path)   
		if lst: 
			for each in lst: 
				spath=path+'/'+each  
				if os.path.isfile(spath):   
					fileobj=string.find(spath,ext)  
					if fileobj != -1: _files_lst.append(spath)   
				fetch(spath) 

def RoadRunner(): 
	while 1: 
		strngToInsert = raw_input ( '\nEnter string to incorporate : ' ) 
		if strngToInsert: break 

	file_extension = raw_input ( 'Enter extension of the files to be updated [.html] : ')
	if not file_extension: file_extension = '.html' 

	while 1: 
		regexp = raw_input ( 'Enter regex string [e.g: <[Bb][oO][dD][yY].*>] : ' ) 
		if regexp: break 

	while 1: 
		update_path = raw_input ( 'Enter path to update [%s] : ' % (os.getcwd()) ) 
		if not update_path: update_path = os.getcwd()  
		if os.path.isdir(update_path): break  

	print "\nYou have entered the following : \n" 
	print "String to incorporate: %s" % (strngToInsert) 
	print "Regex string: %s" % (regexp) 
	print "Path to update: %s\n" % (update_path)

	ok = raw_input("Is this ok?[Y/n] : " )  
	if not ok: ok='Y' 

	if string.lower(ok)!='y': 
		sys.exit(1) 
	else:
		fetch(update_path) 
		compose(strngToInsert,regexp,_files_lst)  


if __name__ == '__main__' : 

	RoadRunner()  
