def VersionFile(file_spec, vtype='copy'):
	import os, shutil

	ok = 0
	if os.path.isfile(file_spec):
		# or do other error checking...
		if vtype not in ('copy', 'rename'):
			vtype = 'copy'

		# determine root file name so the extension doesn't get longer and longer...
		n, e = os.path.splitext(file_spec)

		# is e an integer?
		try:
			num = int(e)
			root = n
		except ValueError:
			root = file_spec

		# find next available file version
		for i in xrange(1000):
			new_file = '%s.%03d' % (root, i)
			if not os.path.isfile(new_file):
				if vtype == 'copy':
					shutil.copy(file_spec, new_file)
				else:
					os.rename(file_spec, new_file)
				ok = 1
				break
	return ok

if __name__ == '__main__':
	# test code (you will need a file named test.txt)
	print VersionFile('test.txt')
	print VersionFile('test.txt')
	print VersionFile('test.txt')
