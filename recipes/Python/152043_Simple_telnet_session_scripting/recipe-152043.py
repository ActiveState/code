#!/usr/local/bin/python 

""" Telnet scripting interface

This class supports simple scripting of a telnet session. When
created, it takes the name of the host and an optional dictionary.
Scripts are passed to the object's RunScript method as a list of 
strings. Here is an example script:

	ru Login:
	w %(user)s
	ru Password:
	w %(pwd)s
	w cd ~/branches/HEAD
	w %(cvslogin)s
	w %(cvsup)s
	# Should do something useful here
	w exit
	c

Which means: 

	Read until "Login:"	
	Write the value associated with the key "user" in the dictionary
	Read until "Password:"
	Write value of key "password"
	Change to $HOME/branches/HEAD
	Write the value of key "cvslogin" (this happens to contain a cvs 
	                                   login command w/ -d option)
	Write the value of key "cvsup" (likewise, a cvs up command)
	(Do nothing, comment)
	Exit the telnet shell
	Close the telnet session
	
Each command is one or two characters, followed by whitespace, followed by
an optional string that serves as a parameter to the command. (Some commands,
eg Read All, do not have commands. For a list of commands that telnetscript
supports, see the definition of self.__functable in the __init__ method
below.

Lines that are blank are ignored, as are lines that begin with "#".

When RunScript returns, it returns a buffer (string) that contains all 
the stuff that was read during the session.

Final note: I commonly assign variables that the script is going to 
expect within the calling namespace, and then pass all local variables
to the script object using vars().
"""

import telnetlib, re

class telnetscript:

	parserx = re.compile( '^\s*(\w+)(?:\s+)?(.*)' )
	fmtrx = re.compile( '(%[^%])' )
	commentrx = re.compile( '^\s+#' )

	def __init__( self, server, data={} ):
		host = telnetlib.Telnet( server )
		self.__host = host
		self.__buffer = ''
		self.__data = data
		
		self.__functable = { 'ru': host.read_until,
		                     'ra': host.read_all,
		                     'rs': host.read_some,
		                     'rve': host.read_very_eager,
		                     're': host.read_eager,
		                     'rl': host.read_lazy,
		                     'rvl': host.read_very_lazy,
		                     'cl': host.close,
		                     'w': self.write }

	def TelnetObject( self ):
		""" Return the underlying telnet object contained by the script class """
		return self.__host
		
	def RunScript( self, script ):
		""" script is a list of strings """
		rBuffer = ''
		
		for line in script:
			# cull out blank lines and comments
			if (not line.strip()) or self.commentrx.search( line ): continue 
			
			m = self.parserx.search( line ).groups()
			if not m: raise 'Badly-formatted script line: %s' % line
			
			if m[1]:
			# If we find a % not followed by another %, apply formatting
				if self.fmtrx.search( m[1] ):
					arg = m[1] % self.__data
				else:
					arg = m[1]
				
				buff = apply( self.__functable[ m[0] ], arg )
			else:
				buff = apply( self.__functable[ m[0] ])
				
			if buff: rBuffer += buff
				
		return rBuffer
			
	def write( self, text ):
		"""Use this instead of directly calling write so we can insert newline"""
		self.__host.write( '%s\n' % text 
