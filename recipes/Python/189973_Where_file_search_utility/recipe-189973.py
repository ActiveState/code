"""Searches a path for a specified file.
"""

__author__ = "Bill McNeill <billmcn@speakeasy.net>"
__version__ = "1.0"

import sys
import os
import os.path
import glob

def help():
	print """\
where (Environment) Filespec

Searches the paths specified in Environment for all files matching Filespec.
If Environment is not specified, the system PATH is used.\
"""

if len(sys.argv) == 3:
	paths = os.environ[sys.argv[1]]
	file = sys.argv[2]
elif len(sys.argv) == 2:
	paths = os.environ["PATH"]
	file = sys.argv[1]
else:
	help()
	sys.exit(0)

for path in paths.split(";"):
	for match in glob.glob(os.path.join(path, file)):
		print match
