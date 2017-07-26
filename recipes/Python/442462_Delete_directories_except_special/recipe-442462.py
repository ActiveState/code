# remove all folders except admin*
# author
# version: 0.1
# date   : October 2005
#----------------------------------------------------------

import os, string, shutil

SETPATH = "c:\Documents and Settings"

files = os.listdir( SETPATH )

for x in files:
	if not x.lower().startswith( 'admin'):
		fullpath = os.path.join( SETPATH, x )
	        if os.path.isdir( fullpath ):
			shutil.rmtree( fullpath )
			print "Removed: ", fullpath, "\n"
