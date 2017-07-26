#!
import string
import gzip
from optparse import OptionParser

#
# version 1.01
#created by T.Newell 06/11/2007
# after searching the web ASPN and not finding a simple example of using gzip to zip a file i created this little gem.
#

def readCommandLine():
	parser = OptionParser()
	#read the options in
	parser.add_option("-f","--Full_file_location",
					dest="File_to_be_run",
					default=r"c:\tn.txt",
					help="This is the fully qualified path name to the file location")

	parser.add_option("-m","--Mode",
					dest="modeTn",
					default="r",
					help="The mode of zip unzip")
	
	parser.add_option("-c","--Compression",
					dest="compress",
					default=9,
					help="The level of compression")
	options, args = parser.parse_args()
	#print options
	return options

def zipit(filename, mode,compress):
	#Saves/Zipps a compressed file to disk
	#
	r_file = open(filename, 'r')
	# this is the zipping bit
	w_file = gzip.GzipFile(filename + '.gz', mode, compress)
	w_file.write(r_file.read())
	w_file.flush()
	w_file.close()
	r_file.close()

def un_zipit(filename,mode):
	#Unzips a compressed file from disk
	#
	#this is the unzipping bit	
	r_file = gzip.GzipFile(filename, mode)
	write_file = string.rstrip(filename, '.gz')
	w_file = open(write_file, 'w')
	w_file.write(r_file.read())
	w_file.close()
	r_file.close()

if __name__ == "__main__":
	#first thing to do is read the options in
	options = readCommandLine()
	if options.modeTn == "r":
		#unzippit mode
		if options.File_to_be_run[-3:] != '.gz':
			# check to see if it has the extension .gz
			print "This " + options.File_to_be_run + " is not a .gz file"
		else:
			#This should now unzipit
			un_zipit(options.File_to_be_run,options.modeTn)
	elif options.modeTn== "wb":
			#this should zipit
			zipit(options.File_to_be_run,options.modeTn,options.compress)
	else:
		# basically the wrong option was passed
		print "ABORT something went wrong"
		sys.exit()
