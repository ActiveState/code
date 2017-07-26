from io import BytesIO
from subprocess import Popen, PIPE
from os import pipe, fdopen
from threading import Thread

class Pipeable( object ):
	def __init__( self ):
		self.output = None
	def _output( self, input = None ):
		return self.output
	def __or__( self, right ):
		if not isinstance( right, Pipeable ): return NotImplemented
		self.output = right._output( self._output() )
		return self

class Shell( Pipeable ):
	def __init__( self, cmd ):
		Pipeable.__init__( self )
		self.cmd = cmd
	def _output( self, input = None ):
		return Popen( self.cmd, stdin = input, stdout = PIPE ).stdout

class ThreadedFilter( Pipeable ):
	def __init__( self, filter ):
		self.filter = filter
		_pipe = pipe()
		self.pipe = fdopen( _pipe[ 1 ], 'w' )
		self.output = fdopen( _pipe[ 0 ], 'r' )
	def _output( self, input = None ):
		def _target():
			_out = self.pipe
			for line in input:
				_out.write( self.filter( line ) )
		Thread( target = _target ).start()
		return self.output

class CachedFilter( Pipeable ):
	def __init__( self, filter ):
		self.filter = filter
	def _output( self, input = None ):
		output = BytesIO()
		for line in input:
			output.write( self.filter( line ) )
		output.seek( 0 )
		return output

class Output( Pipeable ):
	def __init__( self, output ):
		self.output = output

class Print( object ):
	def __ror__( self, left ):
		print left.output.read()

class Write( object ):
	def __init__( self, path ):
		self.path = path
	def __ror__( self, left ):
		f = open( self.path, 'w' )
		while True:
			buf = left.output.read( 1024 )
			if not buf: break
			f.write( buf )
		f.close()
	
if __name__ == '__main__':
	Output( open( "/etc/passwd" ) ) | Shell( "rev" ) | ThreadedFilter( lambda str : str[::-1] ) | CachedFilter( lambda x : x ) | Print()
	
