#parse a python file in a given environment, and get out some results
from os import dirname

def parseFile(filename, envin, envout = {}):
	exec "from sys import path" in envin
	exec "path.append(\"" + dirname(filename) + "\")" in envin
	envin.pop("path")
	lines = open(filename, 'r').read()
	exec lines in envin
	returndict = {}
	for key in envout:
		returndict[key] = envin[key]
	return returndict
