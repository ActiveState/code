import string, sys, os, getopt
from os.path import *

units = 'b'

def print_path (path, bytes):
	if units == 'k':
		print '%-8ld%s' % (bytes / 1024, path)
	elif units == 'm':
		print '%-5ld%s' % (bytes / 1024 / 1024, path)
	else:
		print '%-11ld%s' % (bytes, path)

def dir_size (start, follow_links, my_depth, max_depth):
	total = 0L
	try:
		dir_list = os.listdir (start)
	except:
		if isdir (start):
			print 'Cannot list directory %s' % start
		return 0
	for item in dir_list:
		path = '%s/%s' % (start, item)
		try:
			stats = os.stat (path)
		except:
			print 'Cannot stat %s' % path
			continue
		total += stats[6]
		if isdir (path) and (follow_links or \
			(not follow_links and not islink (path))):
			bytes = dir_size (path, follow_links, my_depth + 1, max_depth)
			total += bytes
			if (my_depth < max_depth):
				print_path (path, bytes)
	return total

def usage (name):
	print "usage: %s [-bkLm] [-d depth] directory [diretory...]" % name
	print '\t-b\t\tDisplay in Bytes (default)'
	print '\t-k\t\tDisplay in Kilobytes'
	print '\t-m\t\tDisplay in Megabytes'
	print '\t-L\t\tFollow symbolic links (Unix only)'
	print '\t-d, --depth\t# of directories down to print (default = 0)'

# main area
follow_links = 0
depth = 0

try:
	opts, args = getopt.getopt (sys.argv[1:], "bkLmd:", ["depth="])
except getopt.GetoptError:
	usage (sys.argv[0])
	sys.exit (1)

for o, a in opts:
	if o == '-b':
		units = 'b'
	elif o == '-k':
		units = 'k'
	elif o == '-L':
		follow_links = 1
	elif o == '-m':
		units = 'm'
	elif o in ('-d', '--depth'):
		try:
			depth = string.atoi (a)
		except:
			pass

if len (args) < 1:
	usage (sys.argv[0])
	sys.exit (1)
else:
	paths = args

for path in paths:
	bytes = dir_size (path, follow_links, 0, depth)
	print_path (path, bytes)
