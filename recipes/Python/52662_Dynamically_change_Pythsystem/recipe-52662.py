def AddSysPath(new_path):
	import sys, os

	# standardise
	new_path = os.path.abspath(new_path)

	# MS-Windows does not respect case
	if sys.platform == 'win32':
		new_path = new_path.lower()

	# disallow bad paths
	do = -1
	if os.path.exists(new_path):
		do = 1
		
		# check against all paths currently available
		for x in sys.path:
			x = os.path.abspath(x)
			if sys.platform == 'win32':
				x = x.lower()
			if new_path in (x, x + os.sep):
				do = 0

		# add path if we don't already have it
		if do:
			sys.path.append(new_path)
			pass

	return do

if __name__ == '__main__':
	# test
	import sys

	print 'Before:'
	for x in sys.path:
		print x

	if sys.platform == 'win32':
		print AddSysPath('c:\\Temp')
		print AddSysPath('c:\\temp')
	else:
		print AddSysPath('usr/lib/my_modules')

	print 'After:'
	for x in sys.path:
		print x
