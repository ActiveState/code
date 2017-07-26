#!/usr/bin/python
# tabify.py -- Convert indentation with spaces to tabs
# 2006-01-23 by Yuce Tekol. www.geocities.com/yucetekol
# Last modification: 2006-07-18

import sys
import os
from stat import ST_MODE
import tokenize

__VERSION__ = "0.5.1"

def tabify(filename):
	mode = os.stat(filename)[ST_MODE]
	os.rename(filename, filename+".bak")
	
	infile = file(filename+".bak")
	outfile = file(filename,"w")
	tokens = tokenize.generate_tokens(infile.readline)
		
	text = []
	indent = 0
	minlineno = 0
	for (toktype, token, start, end, line) in tokens:
		y, x = end
		
		if toktype == tokenize.INDENT:
			indent += 1
		elif toktype == tokenize.DEDENT:
			indent -= 1
		elif y > minlineno:
			minlineno = y
			text += "%s%s\n" % ("\t"*indent,line.strip())
			
	outfile.write("".join(text))
	
	infile.close()
	outfile.close()
	os.chmod(filename, mode)

def main():
	if len(sys.argv) < 2:
		print "usage: %s file1.py file2.py ..." % sys.argv[0]
		sys.exit()
			
	for filename in sys.argv[1:]:
		tabify(filename)
	
if __name__ == "__main__":
	main()
