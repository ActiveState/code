def ParseFile( file ):
	import os
	(root, ext) = os.path.splitext(file)
	(x, name) = os.path.split(root)
		
	# dummy value
	y = '-'		
	parts = []
	while y <> '':
		(x, y) = os.path.split(x)
		parts.append(y)
	parts = parts[:-1]
	if x:
		parts.append(x)
	parts.reverse()

	return (parts, name, ext)

if __name__ == '__main__':
	# test code
	print ParseFile( 'c:/junk.py' )
	print ParseFile( 'junk' )
	print ParseFile( 'c:/test/junk.py.097' )
