from __future__ import generators
import fileinput, glob, string, sys, os, re
from os.path import join


def checkdirname(name):
	"check if directory name matches with the given pattern"
	
	pattern = re.compile(r'^arth(\D*)-d$')
	#print 'checking dirname:', name
	m = pattern.search(name)
	if m is None:
		return False
	else:
		#print 'returning true for', name
		return True

def checkfilename(name):
	"check if file name matches with the given pattern"

	m = re.search('(\D*).xml$', name)
	#print 'checking filename', name
	if m is None:
		return False
	else:
		#print 'returning true for filename', name
		return True
			
def renamedir(dirname, newname):
 	"rename a directory with a given new name"
	os.rename(dirname, newname)
	

def replacestrs(filename):
	"replace a certain type of string occurances in all files in a directory" 
	
	files = glob.glob(filename)
	#print 'files in files:', files
	stext = '-d0'
	rtext = '-r0'
	
	for line in fileinput.input(files,inplace=1):
		
		lineno = 0
  		lineno = string.find(line, stext)
  		if lineno >0:
  			line =line.replace(stext, rtext)
			
  		sys.stdout.write(line)		
	
	

def dirwalk(dir):
    '''walk a directory tree, using a generator, rename certain directories
    replace particular strings in xml files on the way'''
    newname = 'newdir'
    for f in os.listdir(dir):
    	
        fullpath = os.path.join(dir, f)
        
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
        	
        	if checkdirname(f):
        		newname = f[:len(f)-2]+'-r'
        		renamedir(fullpath, os.path.join(dir, newname))
        		fullpath = os.path.join(dir, newname)
        	
        	for x in dirwalk(fullpath):
        			#print 'recursing in subdirectory: ', f , x
        			yield x
        if os.path.isfile(fullpath):
			print 'Saw file', fullpath
			
			if checkfilename(f):
				replacestrs(fullpath)
				
			yield f, fullpath	
        else:
        	
        	yield f, fullpath
      
        
        	
def main():

		
		if len(sys.argv) < 2:
			print 'Usage: Python dirwalkren.py directoryname.'
			sys.exit(1)
		else:
			for dir in dirwalk(sys.argv[1]):
				pass
				
			
if __name__ == '__main__':
	main()        	
        	
        	
        	
        	
        	
        
