"""
Test Regular Expressions

Written by Sunjay Varma -- www.sunjay.ca
"""

import sys, re, argparse, traceback as tb

__version__ = "1.0"

VALID_FLAGS = ['DOTALL', 'I', 'IGNORECASE', 'L', 'LOCALE', 'M', 'MULTILINE', 
				'S', 'T', 'TEMPLATE', 'U', 'UNICODE', 'VERBOSE', 'X']
FLAG_SEP = "|"

def parse_argv(argv):
	parser = argparse.ArgumentParser(description="Test A Regular Expression \
Against Input", prog="Regular Expression Tester")
	parser.add_argument('-f', nargs="?", type=argparse.FileType('r'),
		default=None, help="The input file to use, if omitted, will use \
sys.stdin", dest="inputfile")
	parser.add_argument('-p', nargs="?", type=argparse.FileType('r'),
		default=None, help="The input regular expression as a text from a file",
		dest="regfile")
	parser.add_argument('pattern', type=str, help="The pattern to test", 
		default="", nargs="?")
	parser.add_argument("-m", type=str, help="Flags to include in the regular \
expression. (e.g. VERBOSE|I)", dest="flags", default="")
	parser.add_argument("-i", action="store_true", help="Run an input \
interpreter after reading the input file (if any). This happens automatically \
if there is no input file.", dest="after_input")
	return parser.parse_args(argv)

def get_input(ifile):
	try:
		return ifile.readline()
	except (EOFError, KeyboardInterrupt):
		return None
		
def prompt(ifile=sys.stdin, prompt="> "):
	try:
		print prompt,
		return ifile.readline()
	except (EOFError, KeyboardInterrupt):
		return None

def test_line(prog, line=""):
	try:
		result = prog.match(line)
		if result:
			print "\bHere is the result:"
			for x in ["groups", "start", "end"]:
				print x.capitalize()+"=>", getattr(result, x)()
			print ""
			return True
		else:
			print "No Matches!\n"
			return False
	except:
		tb.print_exc()
		print "\nAn error occurred!"
		return False

def test_file(prog, input_file):
	completed, total = 0, 0
	line = get_input(input_file)
	while line:
		print "Testing '%s'"%line.rstrip()
		completed += int(test_line(prog, line))
		
		total += 1
		line = get_input(input_file)
	
	print "\nCompleted %i Successful Tests Out of %i"%(completed, total)
	return completed, total

def main():
	args = parse_argv(sys.argv[1:])
	# retrieve the flags
	flags = 0
	for flag in (args.flags and args.flags.split(FLAG_SEP) or []):
		if flag in VALID_FLAGS:
			flags |= getattr(re, flag) 
	pat = args.pattern
	if not pat and args.regfile:
		pat = args.regfile.read()
	try:
		prog = re.compile(pat, flags)
	except:
		tb.print_exc()
		print "\nInvalid Pattern"
		sys.exit(0)
	# test the pattern
	print "Testing Pattern:",
	if args.regfile:
		print '\n"""\\\n'+pat, '"""\n'
	else:
		print repr(pat), "\n"
	try:
		if args.inputfile:
			test_file(prog, args.inputfile)
			args.inputfile.close()
		if args.after_input or not args.inputfile:
			if args.inputfile:
				print "\nContinuing with Input Testing..."
			completed, total = 0, 0
			line = prompt()
			while line:
				completed += int(test_line(prog, line))
				total += 1
				line = prompt()
			
			print "\nCompleted %i Successful Tests Out of %i"%(completed, total)
	except KeyboardInterrupt:
		raise SystemExit
	
if __name__ == "__main__": 
	main()
