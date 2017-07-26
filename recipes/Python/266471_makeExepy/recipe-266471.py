"""
makeExe.py
- Simple Python script to automate the creation
  of Python executables using py2exe.

(c) 2004 Premshree Pillai (24/01/04)
http://www.qiksearch.com/
"""

## Run this file from Python root dir

import sys
import re

def getFileName():
	global fileName
	fileName = raw_input("Enter file name (rel or abs path, eg., python/file.py): ")
	try:
		fp = open(fileName)
		fp.close()
	except IOError:
		print "File does not exist!"
		getFileName()

getFileName()

package = re.split(":",fileName)
package = re.split("/",package[len(package) - 1])
package = re.split(".py",package[len(package) - 1])
package = package[0]

def getSetupName():
	global setupName
	setupName = raw_input("Enter name of setup file (or <enter> for default): ")
	if(setupName == ''):
		setupName = "setup.py"
	try:
		fp = open(setupName)
		fp.close()
		flag = raw_input("Setup file exists! Rewrite (0=no; else <enter>)? ")
		if(flag == "1"):
			getSetupName()
	except IOError:
		setupName = setupName

getSetupName()

fp = open(setupName,"w")
temp = """from distutils.core import setup
import py2exe
setup(name = "%s",
     scripts = ["%s"],
)""" % (package,fileName)
fp.write(temp)
fp.close()

sys.argv.append("py2exe")
execfile(setupName)

fp = open(setupName,"w")
temp = ""
fp.write(temp)
fp.close()

print "\n", "Executable created!"
print "Press <enter> to exit..."
if(raw_input()):
	exit
