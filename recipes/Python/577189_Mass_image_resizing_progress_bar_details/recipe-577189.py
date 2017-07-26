#!/usr/bin/env python

from os import *
import sys
try:
	from PIL import Image
except ImportError:
	print "Python image libraries not found!"
	sys.exit()		

# Default options
size=1024,9000
extlist=['.jpg', '.jpeg']
directory=getcwd()
getchild=False

def resize(folder, level=0):
	"Does the actual image scaling action" 
	          	
	tick = unichr(0x2714).encode("utf-8")
	dot= unichr(0x2726).encode("utf-8")	
	unitSegment=5     #The basic unit in the loading bar
	linesPerP=1.0/unitSegment
	
	if path.isdir(folder):						
		imageQue=[item for item in listdir(folder) if path.splitext(item.lower())[1] in extlist]		
		total=len(imageQue)		
		folderData=dot+' '+ folder.split(sep)[-1]
		done=0
		maxImageName=0 #resets to previous image name's length everytime(to clear the exact length) 
		
		for image in imageQue:
			maxImageName= max(maxImageName, len(image))
			percentage= int(float(done)/total*100)
			
			#the dynamic loading bar data 
			sys.stdout.write( "\r{indent}{fold}  [{imgno}] [{bar}] {per}%    {img}".format( 
			indent='   '+' '*level,
			fold=folderData,
			imgno=str(total)+' images',
			bar=('='*int(percentage*linesPerP)).ljust(int(100*linesPerP)),
			per=percentage, 
			img= image.ljust(maxImageName) ))			
			sys.stdout.flush()		
			
			#the resizing process
			maxImageName=len(image)
			image=path.join(folder,image)
			im=Image.open(image)
			im.thumbnail(size, Image.ANTIALIAS)
    			im.save(image, im.format)			
			done+=1
			
		
		#the completed loading bar data	
		sys.stdout.write( "\r{indent}{fold}  [{imgno}] [{alldone}] {clear}\n".format(
		indent='   '+' '*level,
		fold=folderData, 
		alldone=tick, 
		imgno=str(total)+' images',
		clear=' '*(6+maxImageName+int(100*linesPerP))  ))
		
		#attacking sub directories!				
		if getchild:
			for subfolder in listdir(folder):						
				resize(folder+sep+subfolder,level+5)				
				
def invalidArgs():
	print "Invalid arguments!"
	sys.exit()				

def parseArgs():
	"Analyse the commandline parameters; Calls resize function if things are okay "
	arglist=['-d','-o','-e','-c'] # -c is alone (no additional data); others work in pairs
	global size
	global extlist
	global directory
	global getchild
	
	if '--help' in sys.argv or '--start' not in sys.argv:     # --help is the show stopper :)
		print """		
Usage: imageresize --start [options] 
		
Scale images to given size
  * Default directory is current directory (includes subdirectories)
  * Default resize option is '1024' 
    (scale width of image if it exceeds 1024px; retain aspect ratio)
  * Default extensions are jpg, jpeg (not case-sensitive)
  * Overwrites original image
           
Parameters:
  --start              begins the process  
  -d <path>	       <path> is the path to the required directory 	
  -o '<option>'	       <option> can be of the following formats   
     '100'      : scale width of image to 100px
     'x60'      : scale height of image to 60px
     '100x60'   : scale image within given bounds
     (aspect ratio preserved)
  -e <ext1>,<ext2>...  <extn> is any valid extension (.png, .gif) 
  -c                   Scale images in sub-folders  		   			
  --help	       Displays this help
"""
	else:
		sys.argv.remove('--start')
		l=len(sys.argv)
		i=1
		while i<l:
			arg=sys.argv[i]
			if arg in arglist:
				if arg=='-c':     # -c is alone 
					getchild=True
					i+=1
					continue
				elif i+1<l:
					data=sys.argv[i+1]
					if data in arglist or data==None:
						invalidArgs()   #only pairs; no odd args after -c!
					elif arg=='-d':
						if not path.exists(data):
							print "Directory does not exist"
							invalidArgs()
						directory=data	
					elif arg=='-o':				 					
						validOptionChars=[str(letter) for letter in range(0,10)]
						validOptionChars.extend(['x'])
						for letter in data:  #validating option string
							if letter not in validOptionChars:
								invalidArgs()
						if 'x' in data.replace('x',''): 
							invalidArgs()		
						dim=data.split('x')
						if data.startswith('x'): #scale height
							height=int(dim[0])
							size=height*9,height
						elif 'x' not in data:   #scale width
							width=int(dim[0])
							size=width,width*9
						else:   #scale to fit bounding box
							size=int(dim[0]),int(dim[1])				
					else:				
						extlist.extend(data.lower().split(","))
					i+=2  #Done with the pair, move on
				else:
					invalidArgs() #Expected data not found 		
						
			else:  #if a stranger is present in positions where args are expected
				invalidArgs()		
		resize(directory)   #Okies!				

parseArgs() #So lets get started
	
