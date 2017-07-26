import array, cPickle

class pynumgrid:
	'In-memory number array database'
	def __init__( self, schema=None, fname=None ):
		'''schema -> 'field1:atype field2:atype ...' where atype is a
			python array type code (see eg below)'''
		if fname:
			self.load( fname )
		else:
			if type(schema) == str:
				schema = [ f.split(':') for f in schema.split() ]
			self.schema = schema
			self.flist = [ f for f,t in schema ]
			self.data = dict( [(f, array.array(t)) for f,t in schema] )
			self.rowcount = 0
	def insert( self, record, recnum=None ):
		'Insert one record (or append if no rec number)'
		if recnum == None:
			for i, value in enumerate( record ):
				self.data[ self.flist[i] ].append( value )
		else:
			for i, value in enumerate( record ):
				self.data[ self.flist[i] ].insert( value, recnum )
		self.rowcount += 1
	def update( self, record, recnum ):
		'Change the record at recnum with updated values'
		for i, value in enumerate( record ):
			self.data[ self.flist[i] ][ recnum ] = value
	def delete( self, recnum ):
		'Delete the record ar recnum, and return it'
		record = []
		for field in self.flist:
			record.append( self.data[ field ].pop( recnum ) )
		self.rowcount -= 1
		return record
	def extend( self, colset ):
		'Add a set of columns to the database (fast)'
		for i, col in enumerate( colset ):
			self.data[ self.flist[i] ].extend( col )
		self.rowcount += len( colset[0] )
	def select( self, query, ns={} ):
		'Execute a python expression using data and ns namespace'
		ns.update( dict( _en=enumerate, _rc=xrange(self.rowcount),
			array=array.array ) )
		return eval( query, self.data, ns )
	def fetchlist( self, reclist, cols=[] ):
		'Return a list of records given a list of record numbers'
		cols = cols or self.flist
		colset = [ self.data[f] for f in cols ]
		return [ [d[i] for d in colset] for i in reclist ]
	def save( self, fname ):
		'Write the db to disk files (FAST!)'
		cfg = (self.schema, self.rowcount)
		cPickle.dump( cfg, open(fname+'.cfg','wb'), -1 )
		for field in self.flist:
			fh = open( '%s__%s.dat' % (fname,field), 'wb' )
			self.data[ field ].tofile( fh )
	def load( self, fname ):
		'Read and/or build db on to this database (FAST!)'
		cfg = cPickle.load( open(fname+'.cfg','rb') )
		schema, newrowcount = cfg
		if not hasattr( self, 'data' ):
			self.__init__( schema )
		for field in self.flist:
			fh = open( '%s__%s.dat' % (fname,field), 'rb' )
			try: self.data[ field ].fromfile( fh, newrowcount )
			except EOFError: pass
		self.rowcount += newrowcount

if __name__ == '__main__':
	# Test with "prog -i -s" to build then "prog -l -q" to test a query.
	import sys
	# Age (years), height (cm), weight (kg) for a million people:
	pyg = pynumgrid( 'age:B height:B weight:B' )
	blocksize = 10**5
	blocks = 10
	if '-i' in sys.argv:
		agelist = [ (i*1779+517)%80+18 for i in xrange(blocksize) ]
		heightlist = [ (i*5111+711)%90+120 for i in xrange(blocksize) ]
		weightlist = [ (i*3113+797)%100+50 for i in xrange(blocksize) ]
		for j in xrange(blocks):
			pyg.extend( (agelist, heightlist, weightlist) )
	if '-s' in sys.argv:
		pyg.save( '/tmp/pynumgrid' )
	if '-l' in sys.argv:
		pyg.load( '/tmp/pynumgrid' )
	if '-q' in sys.argv:
		print 'The maximum height (in cm) of people in their 30s:',
		print pyg.select('max(height[i] for i in _rc if 29<age[i]<40)')
		print pyg.fetchlist( range(100,110), cols=['weight','height'] )
