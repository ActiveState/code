class NamedShare(type):
	def __init__( cls, name, bases, classdict ):
		super( NamedShare, cls ).__init__( name, bases, classdict )
		cls.__instances = {}
	def __call__( cls, *args, **kw ):
		if kw.has_key( 'share' ):
			key = kw.get( 'share' )
			del( kw['share'] )
		else:
			key = 'default'
		if not cls.__instances.has_key( key ):
			cls.__instances[key] = super( NamedShare, cls ).__call__( *args, **kw )
		return cls.__instances[key]

# Test/Example Code
if __name__ == '__main__':
	
	class sharedDict( dict ):
		__metaclass__ = NamedShare
	
	class SD2( sharedDict ):
		pass
	
	D1 = sharedDict( a='a', b='b', c='c' )
	D2 = sharedDict( share='share2', d='d', e='e', f='f' )
	D3 = sharedDict( share='share3' )
	D4 = sharedDict()
	D5 = sharedDict( share='share3' )
	
	D6 = SD2()
	
	assert ( D2 is not D1 )
	assert ( D3 is not D1 )
	assert ( D3 is not D2 )
	assert ( D4 is D1 )
	assert ( D5 is D3 )
	assert ( D6 is not D1 )
	
	for s in ['g','h','i']:
		sharedDict(share='share3')[s] = s
	
	for s in ['g','h','i']:
		sharedDict(share='share3')[s] = s
	
	print "D1 (", id(D1), ") =", D1
	print "D2 (", id(D2), ") =", D2
	print "D3 (", id(D3), ") =", D3
	print "D4 (", id(D4), ") =", D4
	print "D5 (", id(D5), ") =", D5
	print "D6 (", id(D6), ") =", D6
