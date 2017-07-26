class Pipeable( object ):
	def _other( self, other ):
		self.other = other
	def __iter__( self ):
		for i in self.other:
			yield i
	def __or__( self, right ):
		right._other( self )
		return right

class Filter( Pipeable ):
	def __init__( self, filter ):
		self.filter = filter
	def __iter__( self ):
		for line in self.other:
			yield self.filter( line )

class Cat( Pipeable ):
	def __init__( self, iterable ):
		self.other = iterable

class Reverse( Pipeable ):
	def __iter__( self ):
		for line in self.other:
			yield line[::-1]

if __name__ == '__main__':
	for line in Cat( ('This', 'is', 'just', 'an', 'example') ) | Reverse() | Filter( lambda str : str[::-1] ):
		print line,
	
