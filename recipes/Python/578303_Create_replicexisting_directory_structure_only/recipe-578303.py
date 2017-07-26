#!/usr/bin/python

#===============================================================================
# Creator: ACHAL RASTOGI
# Contact: achal13rastogi@gmail.com
# Date: August 16, 2012 Time: 03:00 Hrs KST
#===============================================================================

import os
import sys

def path_fetch(_seq,_sec):
    free=[]
    never=[]
    tk = _seq
    kt = _sec
    di = os.listdir("%s"%tk)
    
    for file in di:
            if tk[-1] == "/":
                never.extend([kt,file])
                free.extend([tk,file])
                pa = "".join(free)
                ap = "".join(never)
                if os.path.isdir(pa):
                   os.system('cp -r %s %s'%(pa,ap))
		   path_fetch(pa,ap)
                   free=[]
		   never=[]
                else:
#change the file extension ".pl" with the extension of interest, example ".txt", ".doc", ".xls", etc 
		   if ".pl" in pa:                
		   	os.system('cp %s %s'%(pa,ap))
                   	free=[]
                   	never=[]

def main():
    fh=sys.argv[1]
    two=sys.argv[2]
    if os.path.exists(fh):
	if os.path.exists(two):
		print "Program will EXECUTE"
		path_fetch(fh,two)	
	else:
		print "Output path doesn't exist"
       
    else:
       print "Path doesn't exists"
       sys.exit()
       
if __name__=="__main__":
    main()
