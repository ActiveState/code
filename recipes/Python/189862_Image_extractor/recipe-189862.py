import sys, os, string

#write now write only GIF/JPEG

#image types 
imgtypes=['JPG', 'GIF','GIF']

#signature at beginning of file
imgsigs=['JFIF', 'GIF87a', 'GIF89a']

#offset of signatures from
#file beginning
imgsigoffs=[6, 0, 0]

#our marker array
imgmarker=[]

def main():

	if len(sys.argv) < 2:
		print 'Usage: picdumper <file>\n'
		sys.exit(1)

	filename = os.path.abspath(sys.argv[1])

	if not os.path.isfile(filename):
		print 'Error: No such file ', filename
		sys.exit(2)

	#open file in binary mode
	try:
		infile = open(filename, 'rb')
	#dont bother about specific exceptions
	except:
		print 'Could not open file to read !', filename
		sys.exit(3)
		
	if infile is None:
		print 'Error opening file ', filename
		sys.exit(3)

	c = infile.read(1)

	lastmatch=""
	while c != '':

		#look for image sig
		for x in range(0, len(imgsigs)):

			#find if c is first character of imgsig
			sig=imgsigs[x]
			
			if c == sig[0]:
				#find if the rest of imgsig match
				lentoread=len(sig) - 1
				chunk=c + infile.read(lentoread)
				#print chunk
				#matches
				if chunk==sig:
					fpos=int(infile.tell())
					
					#now we are at end of sig, for getting image
					#pos we need to subtract length of sig and offset
					sigpos=fpos - len(sig)
					imgpos=sigpos - imgsigoffs[x]

					#write position and image type to marker
					imgmarker.append((imgpos, imgtypes[x]))
					lastmatch=imgtypes[x]
				else:
					#bug, we need to reset file position
					#to match other sigs correctly if this
					#one does not.
					currpos=int(infile.tell())
					prevpos=currpos-lentoread
					#seek to previous position
					infile.seek(prevpos)
					

		#read next char
		c=infile.read(1)

	posn=int(infile.tell())
	imgmarker.append((posn, lastmatch))

	print imgmarker
	#write images

	#rewind file
	infile.seek(0)

	imgcount=0

	#most collections store image in reverse
	#order that was appended
	x=len(imgmarker)-1

	while x>=1:

		imgcount += 1
		imginfo=imgmarker[x]

		imgposn=imginfo[0]
		imgtype=imginfo[1]

		#this is the tricky part, to get the correct image
		#we need the file posn before previous one!, that
		#is we need to jump a position. Otherwise all images
		#will be junk or of small resolution.
		imginfoprev=imgmarker[x-2]
		imgposnprev=imginfoprev[0]

		#get length in chars
		imglen= imgposn - imgposnprev
		
		#seek to file position
		infile.seek(imgposnprev)
		#read so many chars
		data=infile.read(imglen)

		#create file name
		imgname="image" + str(imgcount) + '.' + string.lower(imgtype)
		try:
			ofile=open(imgname, 'wb')
		except:
			print 'Could not open file ', imgname, ' for writing...\n'
			continue
		
		if ofile is None:
			print 'Error while trying to create file ', imgname, '!\n'
			continue
		else:
			print 'Dumping image file ', imgname, '...\n'
			ofile.write(data)
			ofile.close()

		#previous marker
		x-=1

		
	print 'Dumped ', imgcount, ' images\n'
	
if __name__=="__main__":
	main()
