import os, sys

# get checksums this may take a while
print "Collecting checksums..."
stdin, stdout = os.popen2("md5sum *.txt")
sums = stdout.readlines()

# sorting files
print "Sorting files..."
ls = {}
for s in sums:
	md5, file = s.split()
	# remove the stupid asterisk
	file = file[1:]
	if md5 in ls:
		ls[md5].append(file)
	else:
		ls[md5] = [file]
		
print "Deleting dupes..."
n = 0
for md5 in ls:
	for file in ls[md5][1:]:
		os.remove(file)
		n += 1
print "Operation complete. %d files removed." % n
