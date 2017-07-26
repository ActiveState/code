'''Does tail -f on log files in a given directory. 
The display is in chronological order of the logged lines, 
given that the first column of log files is timestamp.
It can be altered to fit other formats too'''



import time, os, sys, getopt

def Walk( root, recurse=0, pattern='*', return_folders=0 ):
	import fnmatch, os, string
	
	# initialize
	result = []

	# must have at least root folder
	try:
		names = os.listdir(root)
	except os.error:
		return result

	# expand pattern
	pattern = pattern or '*'
	pat_list = string.splitfields( pattern , ';' )
	
	# check each file
	for name in names:
		fullname = os.path.normpath(os.path.join(root, name))

		# grab if it matches our pattern and entry type
		for pat in pat_list:
			if fnmatch.fnmatch(name, pat):
				if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
					result.append(fullname)
				continue
				
		# recursively scan other folders, appending results
		if recurse:
			if os.path.isdir(fullname) and not os.path.islink(fullname):
				result = result + Walk( fullname, recurse, pattern, return_folders )
			
	return result
	
def main():

	dirname = sys.argv[1]
	print dirname
	files = Walk(dirname, 1, '*', 1)
	if len(files) == 0:
		print 'Empty directory!'
		sys.exit(1)
	
		#Set the filename and open the file
	
	for filename in files:
		print 'printing file names', filename
	
	latest = ""
	while 1:
		for filename in files:
			file = open(filename,'r')
			
			
			#Find the size of the file and move to  the end
			st_results = os.stat(filename)
			#print st_results
			st_size = st_results[6]
			#print st_size
			
			file.seek(st_size -124)
			l = file.read()			
			xin = l.find('\n')
			
			l = l[xin:]
			ts = l[0:24]
			ts = ts.strip()
			
			where = file.tell()
			
			if not l:
				time.sleep(1)
				file.seek(where)		
			
			else:
				if ts > latest:
					
					latest = ts.strip()
					print l.strip() #Print the latest logged line
				

if __name__ == '__main__':
	main()
