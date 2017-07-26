#!/usr/bin/env python
import os

# -------------------------------------------
def breadthFirstFileScan( root ) :
	dirs = [root]
	# while we has dirs to scan
	while len(dirs) :
		nextDirs = []
		for parent in dirs :
			# scan each dir
			for f in os.listdir( parent ) :
				# if there is a dir, then save for next ittr
				# if it  is a file then yield it (we'll return later)
				ff = os.path.join( parent, f )
				if os.path.isdir( ff ) :
					nextDirs.append( ff )
				else :
					yield ff
		# once we've done all the current dirs then
		# we set up the next itter as the child dirs 
		# from the current itter.
		dirs = nextDirs

# -------------------------------------------
# an example func that just outputs the files.
def walkbf( path ) :
	for f in breadthFirstFileScan( path ) :
		print f

# ============================================
# as a demo we'll just start from where we 
# were called from.
walkbf( os.getcwd() )
