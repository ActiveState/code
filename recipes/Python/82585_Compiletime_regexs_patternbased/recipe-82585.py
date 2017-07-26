import re

Commands = \
[
	[ 'description of pattern 1', 
		r'X (?P<num>\d),(?P<name>.*)$', 
		aClass.cmd1],
	[ 'pattern 2', 
		r'Widget (?P<part>.*)$', 
		aClass.cmd2]
]

"""
 Clobber each regex str w/compiled version
"""
for cmd in Commands:
	try:
		cmd[1] = re.compile( cmd[1] )
	except:
		print "Bad pattern for %s: %s" % ( cmd[0], cmd[1] )
		assert 0, "Doh!"
		

class myCommands:

	def _dispatch( self, cmdList, str):
		"""
		Find a match for str in the cmdList, and call the 
		  associated method with arguments that are the 
		  matching grouped sub-exprs from the regex.
		"""
		for cmd in cmdList:
			found = cmd[1].match( str) # or .search()
			if found:
				return cmd[2]( self, *found.groups() )
		return None
	
	def runCommand( self, cmd):
		self._dispatch( Commands, cmd)
		
	def cmd1( self, num, name):
		print "The number for %s is %d" % (name, int(num))
		return 42
	def cmdWidget( self, partnum):
		print "Widget serial #: %d" % partnum
	...


"""
Method 2 - instead of a disptatch table, 
  use function attributes.
 Put these fn's in a modules called 'myCommands', for example.
"""
def cmdDoThis( name, num): 
	print "The number for %s is %d" % (name, int(num))
	return 42
cmdDoThis.patt = r'X (?P<num>\d),(?P<name>.*)$'

def cmdWidget( partnum): 
	print "Widget serial #: %d" % partnum
cmdWidget.patt = r'Widget (?P<part>.*)$'

# and later...

import sys
def autoDispatch( str, module=sys.modules[__name__] ):
	for entry in dir(module):
		# use whatever prefix you like, if desired
		if entry.startswith( 'cmd'):
			fn = cmds.__dict__[entry]
			if not fn.regobj: 
				fn.regobj = re.compile( fn.cmd )
			found = fn.regobj.match( str)
			if found:
				return fn( *found.groups() )

import myCommands
...
autoDispatch( 'Widget 1234A', myCommands)
