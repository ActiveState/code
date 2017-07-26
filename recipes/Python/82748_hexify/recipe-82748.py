import sys, os, traceback, getopt 
from types import *

class Display:
	def __init__(self):
		# display stuff
		self.clear		= ''
		self.lines_per_page	= 19
		self.chars_per_line	= 16
		self.oddity		= '.'
		
		self.line_width		= self.chars_per_line * 4 + 10
		self.dash		= '-' * self.line_width

		# other properties
		self.n_lines		= 0
		self.offset		= 0
		self.hand 		= -1
		
	def SetClear(self):
		# platform-dependent command to clear the display
		if sys.platform in ('linux-i386', 'linux2'):
			self.clear = 'clear'
		elif sys.platform in ('win32', 'dos', 'ms-dos'):
			self.clear = 'cls'
		
	def Clear(self):
		# clear screen using system command
		if self.clear:
			os.system(self.clear)
	
	def Header(self):
		# print header
		self.n_lines = 0
		self.Clear()
		print self.file
		print self.dash

	def Footer(self):
		# print footer
		print self.dash
		spacer = ' ' * (self.line_width - 27)
		s = raw_input(spacer + 'jump to... ')
		
		# if entry is...
		#   valid hex --> jump to that position
		#   x, q...   --> quit
		if s:
			s = s.lower().strip()
			if s in ('x', 'q', 'quit', 'exit', 'end'):
				raise 'MyDone'
			for c in s:
				if c not in '0123456789abcdef':
					s = ''
					break
		if s:
			self.offset = eval('int(0x%s)' % s)
			self.hand.seek(self.offset)
		
	def MakeAscii(self, char):
		# ascii representation of character
		ascii = ord(char)
		if ascii < 32 or (ascii > 127 and ascii < 161):
			x = self.oddity
		else:
			x = char
		return x

	def MakeHex(self, char, length):
		# hex representation of character/integer
		if type(char) is StringType:
			char = ord(char)
		x = hex(char)[2:]
		while len(x) < length:
			x = '0' + x
		return x

	def PrintLine(self, l_hex, l_char):
		# output a line
		if len(l_char) > 0:
			while len(l_char) < 16:
				l_hex	+= '   '
				l_char	+= ' '
			print '%s:%s | %s' % (self.MakeHex(self.offset, 6), l_hex, l_char)
			self.offset += self.chars_per_line
			self.n_lines += 1

	def Process(self):
		l_hex, l_char, n_char = '', '', 0
		
		self.hand = open(self.file, 'rb')   
		self.Header()

		while 1:
			# read next character
			n_char += 1
			char = self.hand.read(1)
			if not char:
				break
			
			# accumulate hex and ascii representations
			l_hex	+= ' ' + self.MakeHex(char, 2)
			l_char	+= self.MakeAscii(char)
			
			# line done
			if n_char == self.chars_per_line:
				self.PrintLine(l_hex, l_char)
				
				l_hex, l_char, n_char = '', '', 0

				# end of page
				if self.n_lines == self.lines_per_page:
					self.Footer()
					self.Header()
		self.PrintLine(l_hex, l_char)
		
	def Args(self, args=[]):
		# process command-line options
		try:
			opts, args = getopt.getopt(args, 'hcl:', ['help', 'clear', 'lines='])
		except getopt.error, msg:
			raise 'MyArgError'

		if len(args) > 1:
			raise 'MyArgError'
		self.file = args[0]
		
		for o, a in opts:
			if o in ('-h', '--help'):
				raise 'MyUsage'
			if o in ('-c', '--clear'):
				self.SetClear()
			if o in ('-l', '--lines'):
				self.lines_per_page	= int(a)

def Usage():
	print """
hexify 1.01
(C) 2001 Robin Parmar <robin.escalation@ACM.org>

Displays a hex dump of specified file.
After each page, you are prompted:
* tap <enter> to continue
* type <q>, <quit>, <x>, or <exit> to bail out
* type in hex code to jump to that location

"I want to hexify!"

usage:
python hexify.py [-h] [--help] [-c] [--clear] [-l<n>] [--lines=<n>] <file>

-h or --help: prints this message
-c or --clear: clears screen between pages (if supported)
-l or --lines: specifies number of lines per page
"""
    
if __name__ == '__main__':
	# this program is designed to run from the command-line
	code = 0
	try:
		d = Display()
		d.Args(sys.argv[1:])
		d.Process()
	except 'MyArgError':
		print '\n[incorrect command-line options]'
		Usage()
		code = 1
	except 'MyUsage':
		print '\n[requested usage info]'
		Usage()
	except 'MyDone':
		print '\n[interrupted by user]'
	except KeyboardInterrupt:
		print '\n[interrupted by user]'
	except:
		# unexpected error
		traceback.print_exc()
		code = 2
	sys.exit(code)
